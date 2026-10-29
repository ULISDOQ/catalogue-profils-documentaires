#!/usr/bin/env python3
"""Prepare a local documentary TAG candidate; never sends document content over network."""
import argparse
import hashlib
import json
from pathlib import Path

def make_tag(family, markers, geometry=None):
    cleaned = sorted(set(m.strip().casefold() for m in markers if m.strip()))
    if not cleaned:
        raise ValueError("At least one non-empty marker is required")
    descriptor = {"schema": "ulisdoq.tag-candidate.v0", "family": family,
                  "text_markers": cleaned, "geometry": geometry or []}
    canonical = json.dumps(descriptor, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    fingerprint = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return {"tag_id": "ULISDOQ-TAG-CANDIDATE-" + fingerprint[:16].upper(),
            "status": "CANDIDATE_UNQUALIFIED", "descriptor": descriptor,
            "descriptor_sha256": fingerprint,
            "matching_status": "NOT_CHECKED",
            "warning": "Descriptor hash is not proof of format identity; no calibrated matching."}

def main():
    p = argparse.ArgumentParser(description="Offline editor for documentary TAG candidates")
    p.add_argument("--family", required=True)
    p.add_argument("--marker", action="append", default=[], help="Non-personal, stable document marker; repeatable")
    p.add_argument("--geometry-json", type=Path, help="Optional local JSON array of non-sensitive geometry descriptors")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    geometry = json.loads(args.geometry_json.read_text(encoding="utf-8")) if args.geometry_json else []
    if not isinstance(geometry, list):
        p.error("geometry-json must contain a JSON array")
    try:
        tag = make_tag(args.family, args.marker, geometry)
    except ValueError as exc:
        p.error(str(exc))
    args.output.write_text(json.dumps(tag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(tag["tag_id"])

if __name__ == "__main__":
    main()
