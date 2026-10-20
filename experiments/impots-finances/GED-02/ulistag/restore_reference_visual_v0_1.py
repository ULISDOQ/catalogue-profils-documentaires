#!/usr/bin/env python3
"""Restore immutable GED-02 visual-keypoints reference from versioned parts.

This does not rebuild or recalibrate the reference. It only decodes the
canonical artifact and verifies its SHA-256 before writing it.
"""
from __future__ import annotations
import argparse, base64, hashlib, zlib
from pathlib import Path

EXPECTED_SHA256="8950bbaf084e02ceab841835e72287a369cc77e999332af55c1c893dd7704e24"
EXPECTED_SIZE=70043
PARTS=[
 "reference_visual_v0_1.zlib.b64.part01",
 "reference_visual_v0_1.zlib.b64.part02",
 "reference_visual_v0_1.zlib.b64.part03",
 "reference_visual_v0_1.zlib.b64.part04",
]

ap=argparse.ArgumentParser()
ap.add_argument("--parts-dir",type=Path,default=Path(__file__).resolve().parent)
ap.add_argument("--output",type=Path,required=True)
args=ap.parse_args()

encoded="".join((args.parts_dir/p).read_text(encoding="ascii").strip() for p in PARTS)
try:
    raw=zlib.decompress(base64.b64decode(encoded,validate=True))
except Exception as exc:
    raise SystemExit(f"FAIL_CLOSED: canonical artifact decode failed: {type(exc).__name__}") from exc

digest=hashlib.sha256(raw).hexdigest()
if digest != EXPECTED_SHA256 or len(raw) != EXPECTED_SIZE:
    raise SystemExit(f"FAIL_CLOSED: canonical artifact integrity mismatch sha256={digest} size={len(raw)}")

if args.output.exists():
    existing=hashlib.sha256(args.output.read_bytes()).hexdigest()
    if existing != EXPECTED_SHA256:
        raise SystemExit(f"FAIL_CLOSED: existing reference drift sha256={existing}")
    print(f"REFERENCE_ALREADY_CONFORMANT sha256={existing}")
else:
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_bytes(raw)
    print(f"REFERENCE_RESTORED sha256={digest} size={len(raw)}")
