#!/usr/bin/env python3
"""GED-02 phase-1 candidate: multi-page layout-density ULISTAG matcher."""
import argparse
import base64
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps


def render_pdf(pdf_path: Path, dpi: int, out_dir: Path):
    exe = shutil.which("pdftoppm")
    if not exe:
        raise SystemExit("pdftoppm is required by this candidate implementation")
    prefix = out_dir / "page"
    subprocess.run(
        [exe, "-png", "-r", str(dpi), str(pdf_path), str(prefix)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    return sorted(out_dir.glob("page-*.png"))


def page_descriptor(path: Path, crop_fraction: float, grid_w: int, grid_h: int):
    im = Image.open(path).convert("L")
    w, h = im.size
    c = crop_fraction
    im = im.crop((int(c*w), int(c*h), int((1-c)*w), int((1-c)*h)))
    im = ImageOps.autocontrast(im)
    arr = 1.0 - np.asarray(im, dtype=np.float32) / 255.0
    small = Image.fromarray((arr * 255).astype(np.uint8)).resize(
        (grid_w, grid_h), Image.Resampling.BOX
    )
    return np.asarray(small, dtype=np.float32).ravel() / 255.0


def observe(pdf_path: Path, ref):
    cfg = ref["render"]
    desc = ref["descriptor"]
    with tempfile.TemporaryDirectory(prefix="ulistag-ged02-") as td:
        pages = render_pdf(pdf_path, int(cfg["dpi"]), Path(td))
        vector = np.concatenate([
            page_descriptor(
                p,
                float(cfg["crop_fraction"]),
                int(desc["grid_width"]),
                int(desc["grid_height"]),
            )
            for p in pages
        ]) if pages else np.array([], dtype=np.float32)
    norm = float(np.linalg.norm(vector))
    if norm:
        vector = vector / norm
    return {"page_count": len(pages), "vector": vector}


def compare(pdf_path: Path, ref):
    obs = observe(pdf_path, ref)
    if ref.get("reference_vector_encoding") != "float32-le-base64":
        raise SystemExit("unsupported reference vector encoding")
    raw = base64.b64decode(ref["reference_vector_b64"])
    ref_vec = np.frombuffer(raw, dtype="<f4")
    if len(ref_vec) != int(ref["reference_vector_length"]):
        raise SystemExit("reference vector length mismatch")
    if obs["page_count"] != int(ref["page_count"]) or len(obs["vector"]) != len(ref_vec):
        similarity = 0.0
        status = "UNKNOWN"
    else:
        similarity = float(np.dot(obs["vector"], ref_vec))
        threshold = float(ref["decision_policy"]["candidate_min_cosine_similarity"])
        status = "MATCH_CANDIDATE" if similarity >= threshold else "UNKNOWN"
    return {
        "status": status,
        "ulistag_id": ref["ulistag_id"],
        "page_count_observed": obs["page_count"],
        "similarity": round(similarity, 6),
        "threshold": ref["decision_policy"]["candidate_min_cosine_similarity"],
        "qualification": "NONE",
        "score_semantics": ref["decision_policy"]["score_semantics"],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("document", type=Path)
    ap.add_argument("--reference", type=Path, required=True)
    args = ap.parse_args()
    ref = json.loads(args.reference.read_text(encoding="utf-8"))
    print(json.dumps(compare(args.document, ref), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
