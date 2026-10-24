#!/usr/bin/env python3
"""GED-04 metadata-only discovery helper.

Reads directory entries and stat metadata only.
It never opens document files and never reads file contents.
MIME estimates are extension-based via mimetypes.guess_type().
"""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
from collections import Counter, defaultdict
from pathlib import Path

DOC_EXTENSIONS = {
    ".pdf", ".jpg", ".jpeg", ".png", ".webp", ".heic",
    ".doc", ".docx", ".odt", ".xls", ".xlsx", ".ods",
    ".txt", ".rtf", ".csv", ".eml", ".msg", ".xml", ".json",
}

SENSITIVE_TOKENS = {
    "impot", "impots", "fiscal", "tax", "banque", "bank", "rib", "iban",
    "sante", "santé", "medical", "medicale", "médical", "mutuelle",
    "ordonnance", "analyse", "laboratoire", "paie", "salaire",
    "identite", "identité", "passeport", "carte", "securite-sociale",
    "sécurité-sociale", "caf", "cpam",
}

FAMILY_HINTS = [
    ("COURRIEL", {".eml", ".msg"}),
    ("PDF_DOCUMENT", {".pdf"}),
    ("IMAGE_DOCUMENT", {".jpg", ".jpeg", ".png", ".webp", ".heic"}),
    ("OFFICE_TEXT", {".doc", ".docx", ".odt", ".rtf"}),
    ("SPREADSHEET", {".xls", ".xlsx", ".ods", ".csv"}),
    ("PLAIN_TEXT", {".txt"}),
    ("STRUCTURED_DATA", {".xml", ".json"}),
]

def sha16(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", "surrogateescape")).hexdigest()[:16]

def estimate_family(ext: str) -> str:
    for family, exts in FAMILY_HINTS:
        if ext in exts:
            return family
    return "OTHER"

def privacy_risk(name: str) -> str:
    folded = name.casefold()
    return "POTENTIAL_SENSITIVE_FILENAME" if any(tok in folded for tok in SENSITIVE_TOKENS) else "UNDETERMINED"

def size_band(size: int) -> str:
    if size < 100_000:
        return "<100KB"
    if size < 1_000_000:
        return "100KB-1MB"
    if size < 10_000_000:
        return "1MB-10MB"
    return ">=10MB"

def inventory(root: Path, recursive: bool):
    rows = []
    iterator = root.rglob("*") if recursive else root.iterdir()
    for p in sorted(iterator, key=lambda x: str(x).casefold()):
        try:
            if not p.is_file():
                continue
            st = p.stat()
        except OSError:
            continue
        ext = p.suffix.casefold()
        if ext not in DOC_EXTENSIONS:
            continue
        mime, _ = mimetypes.guess_type(p.name)
        rel = str(p.relative_to(root))
        rows.append({
            "local_id": "GED04-" + sha16(rel),
            "relative_name": rel,
            "extension": ext or None,
            "size_bytes": st.st_size,
            "size_band": size_band(st.st_size),
            "mime_estimate_from_extension": mime,
            "family_estimate": estimate_family(ext),
            "privacy_risk": privacy_risk(p.name),
        })
    return rows

def summarize(rows):
    by_family = Counter(r["family_estimate"] for r in rows)
    by_ext = Counter(r["extension"] for r in rows)
    risky = sum(r["privacy_risk"] != "UNDETERMINED" for r in rows)
    shortlist = []
    grouped = defaultdict(list)
    for r in rows:
        grouped[r["family_estimate"]].append(r)
    for family, items in sorted(grouped.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        if family == "OTHER":
            continue
        examples = []
        for r in items[:5]:
            examples.append({
                "local_id": r["local_id"],
                "extension": r["extension"],
                "size_band": r["size_band"],
                "privacy_risk": r["privacy_risk"],
            })
        shortlist.append({
            "family_estimate": family,
            "count": len(items),
            "examples_redacted": examples,
            "ged04_interest": (
                "HIGH" if family in {"PDF_DOCUMENT","IMAGE_DOCUMENT","OFFICE_TEXT","SPREADSHEET","STRUCTURED_DATA"}
                else "LOW_ALREADY_EXPLORED" if family == "COURRIEL"
                else "MEDIUM"
            ),
        })
    return {
        "status": "METADATA_ONLY_DISCOVERY",
        "document_count": len(rows),
        "family_counts": dict(sorted(by_family.items())),
        "extension_counts": dict(sorted((k or "", v) for k,v in by_ext.items())),
        "potential_sensitive_filename_count": risky,
        "candidate_shortlist": shortlist,
        "content_read": False,
        "network_used": False,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source", type=Path, help="PHONE_DOWNLOADS_DIRECTORY")
    ap.add_argument("--recursive", action="store_true")
    ap.add_argument("--inventory-out", type=Path, default=Path("/tmp/ged04-metadata-inventory.json"))
    ap.add_argument("--summary-out", type=Path, default=Path("/tmp/ged04-candidate-summary.json"))
    args = ap.parse_args()

    root = args.source.expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"SOURCE_NOT_DIRECTORY: {root}")

    rows = inventory(root, args.recursive)
    args.inventory_out.write_text(json.dumps({
        "source": str(root),
        "scope": "METADATA_ONLY",
        "content_read": False,
        "files": rows,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = summarize(rows)
    args.summary_out.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
