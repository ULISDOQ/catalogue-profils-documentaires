#!/usr/bin/env python3
"""Client minimal ULISDOQ -> invoice2data. Local only; JSON stdout, no network."""
import argparse
import hashlib
import json
import sys
from datetime import date, datetime
from importlib import import_module
from pathlib import Path

LOCAL_READERS = {
    "pdftotext": "pdftotext",
    "tesseract": "tesseract",
    "pdfminer": "pdfminer_wrapper",
    "pdfplumber": "pdfplumber",
    "text": "text",
    "ocrmypdf": "ocrmypdf",
}

def resolve_reader(name):
    if name not in LOCAL_READERS:
        raise ValueError("Unsupported local reader: " + name +
                         ". Available names: " + ", ".join(LOCAL_READERS))
    module = import_module("invoice2data.input." + LOCAL_READERS[name])
    if not callable(getattr(module, "to_text", None)):
        raise RuntimeError("Reader does not provide to_text: " + name)
    return module

def main():
    parser = argparse.ArgumentParser(description="Extract a local invoice with ULISDOQ templates")
    parser.add_argument("document", type=Path)
    parser.add_argument("--templates", type=Path, required=True,
                        help="Directory containing the ULISDOQ invoice2data templates to use")
    parser.add_argument("--reader", default="tesseract",
                        help="Local invoice2data reader: " + ", ".join(LOCAL_READERS))
    args = parser.parse_args()
    if not args.document.is_file() or not args.templates.is_dir():
        print(json.dumps({"status": "ERROR", "reason": "document or template directory missing"}))
        return 2
    digest = hashlib.sha256(args.document.read_bytes()).hexdigest()
    try:
        reader_module = resolve_reader(args.reader)
        from invoice2data import extract_data
        from invoice2data.extract.loader import read_templates
        templates = read_templates(str(args.templates))
        if not templates:
            raise RuntimeError("no templates loaded")
        result = extract_data(str(args.document), templates=templates, input_module=reader_module)
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
