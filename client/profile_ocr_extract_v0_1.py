#!/usr/bin/env python3
"""ULISDOQ profile-driven OCR geometric extraction candidate v0.1.

This adapter is intentionally conservative:
- profile discovery is explicit through the ULISDOQ registry;
- field geometry comes from a versioned binding derived from the official blank form;
- OCR reads only bound value regions;
- no ground-truth file is accepted or read;
- output is validated against the declared semantic schema.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def tesseract_version() -> str:
    proc = subprocess.run(
        ["tesseract", "--version"],
        capture_output=True,
        text=True,
        timeout=15,
    )
    if proc.returncode:
        raise RuntimeError("TESSERACT_NOT_AVAILABLE")
    return (proc.stdout or proc.stderr).splitlines()[0]


def resolve_profile(registry: dict, format_tag_id: str) -> dict:
    matches = [
        item
        for item in registry.get("profiles", [])
        if item.get("format_tag_id") == format_tag_id
    ]
    if len(matches) != 1:
        raise RuntimeError(f"PROFILE_DISCOVERY_EXPECTED_ONE_GOT_{len(matches)}")
    return matches[0]


def ocr_region(page, region_norm, dpi: int, languages, psm: int):
    import fitz

    x0n, y0n, x1n, y1n = region_norm
    clip = fitz.Rect(
        x0n * page.rect.width,
        y0n * page.rect.height,
        x1n * page.rect.width,
        y1n * page.rect.height,
    )
    scale = dpi / 72.0
    pix = page.get_pixmap(
        matrix=fitz.Matrix(scale, scale),
        clip=clip,
        colorspace=fitz.csGRAY,
        alpha=False,
    )
    proc = subprocess.run(
        [
            "tesseract",
            "stdin",
            "stdout",
            "-l",
            "+".join(languages),
            "--psm",
            str(psm),
            "tsv",
        ],
        input=pix.tobytes("png"),
        capture_output=True,
        timeout=60,
    )
    if proc.returncode:
        raise RuntimeError("OCR_FAILED")

    tokens = []
    for line in proc.stdout.decode("utf-8", "replace").splitlines()[1:]:
        cols = line.split("\t", 11)
        if len(cols) < 12 or not cols[11].strip():
            continue
        try:
            confidence = float(cols[10])
        except ValueError:
            confidence = -1
        if confidence < 0:
            continue
        tokens.append({"text": cols[11].strip(), "confidence": confidence})

    raw = " ".join(token["text"] for token in tokens).strip()
    confidence = (
        sum(token["confidence"] for token in tokens) / len(tokens)
        if tokens
        else None
    )
    return raw, confidence


def parse_value(raw: str, parser: str):
    value = " ".join(raw.split()).strip()
    if not value:
        return "UNREADABLE", None

    if parser == "strict_text":
        return "VALUE", value

    if parser == "strict_integer":
        candidates = re.findall(
            r"(?<!\w)[+-]?\d(?:[\d\s.\u00a0]*\d)?(?!\w)",
            value,
        )
        normalized = []
        for candidate in candidates:
            number = re.sub(r"[\s.\u00a0]", "", candidate)
            if re.fullmatch(r"[+-]?\d+", number):
                normalized.append(number)
        normalized = list(dict.fromkeys(normalized))
        if len(normalized) == 1:
            return "VALUE", int(normalized[0])
        if len(normalized) > 1:
            return "AMBIGUOUS", None
        return "UNREADABLE", None

    return "UNREADABLE", None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("document", type=Path)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--format-tag-id", required=True)
    parser.add_argument("--schema", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    document = args.document.resolve()
    registry_path = args.registry.resolve()
    schema_path = args.schema.resolve()

    if not document.is_file():
        raise SystemExit("document missing")

    registry = load_json(registry_path)
    entry = resolve_profile(registry, args.format_tag_id)

    profile_path = (repo / entry["profile_path"]).resolve()
    profile = load_json(profile_path)
    if (
        profile.get("profile_id") != entry.get("profile_id")
        or profile.get("version") != entry.get("profile_version")
    ):
        raise RuntimeError("PROFILE_IDENTITY_DRIFT")
    if profile.get("format_tag_id") != args.format_tag_id:
        raise RuntimeError("PROFILE_FORMAT_TAG_DRIFT")

    extraction = profile.get("extraction") or {}
    binding_rel = extraction.get("binding")
    if not binding_rel:
        raise RuntimeError("PROFILE_BINDING_MISSING")

    binding_path = (profile_path.parent / binding_rel).resolve()
    binding = load_json(binding_path)
    if binding.get("profile_id") != profile["profile_id"]:
        raise RuntimeError("BINDING_PROFILE_DRIFT")

    import fitz

    document_pdf = fitz.open(document)
    reader = binding["reader_contract"]
    dpi = int(reader.get("render_dpi", 240))
    languages = reader.get("languages", ["fra", "eng"])

    fields = []
    reader_version = tesseract_version()
    for spec in binding["fields"]:
        page_number = int(spec["page"])
        if page_number < 1 or page_number > len(document_pdf):
            fields.append(
                {
                    "official_id": spec["official_id"],
                    "official_label": spec["official_label"],
                    "page": page_number,
                    "status": "UNREADABLE",
                    "value": None,
                    "evidence": {"reason": "page_missing"},
                }
            )
            continue

        psm = int(
            reader.get("text_psm", 6)
            if spec["parser"] == "strict_text"
            else reader.get("numeric_psm", 7)
        )
        try:
            raw, confidence = ocr_region(
                document_pdf[page_number - 1],
                spec["value_region_norm"],
                dpi,
                languages,
                psm,
            )
            status, value = parse_value(raw, spec["parser"])
            evidence = {
                "reader": reader_version,
                "confidence": confidence,
                "region_norm": spec["value_region_norm"],
                "parser": spec["parser"],
            }
        except Exception as exc:
            status, value = "UNREADABLE", None
            evidence = {
                "reader": reader_version,
                "error_type": type(exc).__name__,
                "reason": str(exc)[:200],
                "region_norm": spec["value_region_norm"],
                "parser": spec["parser"],
            }

        fields.append(
            {
                "official_id": spec["official_id"],
                "official_label": spec["official_label"],
                "page": page_number,
                "status": status,
                "value": value,
                "evidence": evidence,
            }
        )

    result = {
        "document_profile_id": profile["profile_id"],
        "specimen_id": document.stem,
        "profile_decision": "MATCH_CANDIDATE",
        "method_qualification": "PHASE1_CANDIDATE",
        "fields": fields,
        "traceability": {
            "format_tag_id": args.format_tag_id,
            "profile_version": profile["version"],
            "registry_sha256": sha256(registry_path),
            "profile_sha256": sha256(profile_path),
            "binding_id": binding["binding_id"],
            "binding_sha256": sha256(binding_path),
            "source_sha256": sha256(document),
            "semantic_schema_sha256": sha256(schema_path),
            "ground_truth_access": "NONE",
        },
    }

    from jsonschema import validate

    validate(result, load_json(schema_path))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
