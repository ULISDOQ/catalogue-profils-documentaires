#!/usr/bin/env python3
"""Client minimal ULISDOQ -> invoice2data. Local only; JSON stdout, no network."""
import argparse
import hashlib
import json
import sys
from datetime import date, datetime
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Extract a local invoice with an ULISDOQ template")
    parser.add_argument("document", type=Path)
    parser.add_argument("--templates", type=Path, default=Path(__file__).resolve().parents[1] / "templates")
    parser.add_argument("--reader", default="tesseract", help="invoice2data input reader; e.g. tesseract, pdfium, text")
    args = parser.parse_args()
    if not args.document.is_file() or not args.templates.is_dir():
        print(json.dumps({"status": "ERROR", "reason": "document or template directory missing"}))
        return 2
    digest = hashlib.sha256(args.document.read_bytes()).hexdigest()
    try:
        from invoice2data import extract_data
        from invoice2data.extract.loader import read_templates
        templates = read_templates(str(args.templates))
        if not templates:
            raise RuntimeError("no templates loaded")
        result = extract_data(str(args.document), templates=templates, input_module=args.reader)
        if not result:
            print(json.dumps({"status": "NO_MATCH", "source_sha256": digest, "engine": "invoice2data",
                              "reader": args.reader, "data": None}, ensure_ascii=False))
            return 1
        def encode(obj):
            if isinstance(obj, (date, datetime)):
                return obj.isoformat()
            raise TypeError(f"non-JSON value: {type(obj).__name__}")
        print(json.dumps({"status": "EXTRACTED_UNVERIFIED", "source_sha256": digest,
                          "engine": "invoice2data", "reader": args.reader,
                          "data": result}, ensure_ascii=False, default=encode, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"status": "ERROR", "source_sha256": digest,
                          "error_type": type(exc).__name__, "reason": str(exc)}, ensure_ascii=False))
        return 2

if __name__ == "__main__":
    sys.exit(main())
