#!/usr/bin/env python3
"""Generic ULISDOQ profile resolver candidate v0.1.

No document-family exception is coded here. Resolution is driven only by
versioned registry declarations.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_container_native(registry: dict, media_type: str, extension: str):
    media_type = media_type.casefold().strip()
    extension = extension.casefold().strip()
    matches = []
    for entry in registry.get("profiles", []):
        recognition = entry.get("recognition") or {}
        if recognition.get("mode") != "CONTAINER_NATIVE":
            continue
        contract = recognition.get("container_contract") or {}
        media_types = {str(v).casefold() for v in contract.get("media_types", [])}
        extensions = {str(v).casefold() for v in contract.get("extensions", [])}
        media_ok = not media_types or media_type in media_types
        extension_ok = not extensions or extension in extensions
        if media_ok and extension_ok:
            matches.append(entry)
    return matches


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", type=Path, required=True)
    ap.add_argument("--media-type", required=True)
    ap.add_argument("--extension", default="")
    args = ap.parse_args()
    matches = resolve_container_native(load(args.registry), args.media_type, args.extension)
    status = "MATCH" if len(matches) == 1 else ("UNKNOWN" if not matches else "AMBIGUOUS")
    print(json.dumps({
        "status": status,
        "candidate_count": len(matches),
        "profiles": [
            {
                "profile_id": m.get("profile_id"),
                "profile_version": m.get("profile_version"),
                "profile_path": m.get("profile_path"),
            }
            for m in matches
        ],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
