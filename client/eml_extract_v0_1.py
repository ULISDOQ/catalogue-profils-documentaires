#!/usr/bin/env python3
"""GED-03 local EML normalizer candidate v0.1.

Local-only, stdlib MIME parsing. It never executes attachments and never uses
OCR, visual matching, LLMs, or network access.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from email import policy
from email.parser import BytesParser
from email.utils import getaddresses
from pathlib import Path


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def addresses(message, header: str):
    values = [str(v) for v in message.get_all(header, [])]
    return [addr for _, addr in getaddresses(values) if addr]


def all_defects(message):
    defects = []
    for part in message.walk():
        for defect in getattr(part, "defects", ()):
            defects.append(type(defect).__name__)
    return sorted(set(defects))


def classify(message, required_headers):
    present = {name.casefold() for name in message.keys()}
    if not present:
        return "INVALID", ["NO_RFC_STYLE_HEADERS"]

    missing = [h for h in required_headers if h.casefold() not in present]
    defects = all_defects(message)
    close_boundary = "CloseBoundaryNotFoundDefect" in defects

    if close_boundary:
        # Generic distinction: structurally identified message + premature MIME
        # end is treated as TRUNCATED; otherwise the container is MALFORMED.
        return ("TRUNCATED" if not missing else "MALFORMED"), defects + [
            "MISSING_REQUIRED_HEADER:" + h for h in missing
        ]

    if defects:
        return "MALFORMED", defects + [
            "MISSING_REQUIRED_HEADER:" + h for h in missing
        ]

    if missing:
        return "INVALID", ["MISSING_REQUIRED_HEADER:" + h for h in missing]

    return "PARSED", []


def body_text(message):
    try:
        part = message.get_body(preferencelist=("plain",))
    except Exception:
        part = None
    if part is None:
        return None
    try:
        return part.get_content()
    except Exception:
        return None


def attachment_rows(message):
    rows = []
    for part in message.iter_attachments():
        payload = part.get_payload(decode=True)
        rows.append({
            "filename": part.get_filename(),
            "content_type": part.get_content_type(),
            "disposition": part.get_content_disposition(),
            "size_bytes": len(payload) if payload is not None else None,
        })
    return rows


def normalize(document: Path, profile: dict):
    raw = document.read_bytes()
    message = BytesParser(policy=policy.default).parsebytes(raw)
    required_headers = (
        profile.get("container_validation", {}).get("required_headers")
        or ["From", "To", "Subject"]
    )
    parse_status, defects = classify(message, required_headers)

    mime_structure = [part.get_content_type() for part in message.walk()]
    html_present = any(
        part.get_content_type() == "text/html" for part in message.walk()
    )

    result = {
        "specimen_id": document.stem,
        "parse_status": parse_status,
        "message": {
            "message_id": str(message["Message-ID"]) if message["Message-ID"] else None,
            "date": str(message["Date"]) if message["Date"] else None,
            "from": addresses(message, "From"),
            "to": addresses(message, "To"),
            "cc": addresses(message, "Cc"),
            "subject": str(message["Subject"]) if message["Subject"] else None,
            "body_text": body_text(message),
            "body_html_present": html_present,
            "mime_structure": mime_structure,
        },
        "attachments": attachment_rows(message),
        "traceability": {
            "source_sha256": sha256_bytes(raw),
            "parser": "python_stdlib_email.policy.default",
            "profile_id": profile.get("profile_id"),
            "profile_version": profile.get("version"),
            "parser_defects": defects,
            "network_used": False,
            "ocr_used": False,
            "visual_matcher_used": False,
            "llm_used": False,
            "attachment_execution": False,
        },
    }
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("document", type=Path)
    ap.add_argument("--profile", type=Path, required=True)
    ap.add_argument("--schema", type=Path, required=True)
    args = ap.parse_args()

    if not args.document.is_file():
        raise SystemExit("document missing")

    profile = load_json(args.profile)
    result = normalize(args.document, profile)

    try:
        from jsonschema import validate
        validate(result, load_json(args.schema))
    except ImportError:
        raise SystemExit("jsonschema missing from authorized execution environment")

    result["traceability"]["schema_validated"] = True
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    sys.exit(main())
