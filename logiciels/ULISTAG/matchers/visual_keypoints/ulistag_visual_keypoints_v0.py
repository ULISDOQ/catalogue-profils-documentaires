#!/usr/bin/env python3
"""ULISTAG visual-keypoints candidate v0.1.

Reusable document-layout recognition from rendered PDF pages using ORB keypoints,
Hamming descriptor matching and RANSAC homography coherence.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

import cv2
import fitz
import numpy as np

SCHEMA = "ulistag-visual-keypoints/0.1"

def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def render_pdf(path: Path, dpi: int):
    doc=fitz.open(path)
    mat=fitz.Matrix(dpi/72.0, dpi/72.0)
    pages=[]
    for page in doc:
        pix=page.get_pixmap(matrix=mat, colorspace=fitz.csGRAY, alpha=False)
        arr=np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width)
        pages.append(arr.copy())
    return pages

def orb(nfeatures=5000):
    return cv2.ORB_create(nfeatures=nfeatures, scaleFactor=1.2, nlevels=8,
                          edgeThreshold=15, patchSize=31, fastThreshold=10)

def observe_page(img, nfeatures=5000):
    kps, desc=orb(nfeatures).detectAndCompute(img, None)
    if desc is None:
        return [], np.empty((0,32), dtype=np.uint8)
    return kps, desc

def build_reference(pdf_path: Path, ulistag_id: str, dpi: int, keep_per_page: int, calibration_path: Path | None = None):
    pages=render_pdf(pdf_path, dpi)
    calibration_pages=render_pdf(calibration_path, dpi) if calibration_path else None
    out={
        "schema_version":SCHEMA,
        "ulistag_id":ulistag_id,
        "status":"CANDIDATE_UNQUALIFIED",
        "observer":{"type":"pdf_render_grayscale","dpi":dpi},
        "matcher":{"type":"orb_hamming_homography","ratio_test":0.72,"ransac_reproj_px":5.0},
        "decision_policy":{"min_good_matches":10,"min_inliers":8,"min_inlier_ratio":0.55,"min_matching_pages_ratio":0.75},
        "reference":{"page_count":len(pages),"source_sha256":sha256_file(pdf_path),"pages":[]},
        "calibration":{"source_sha256":sha256_file(calibration_path)} if calibration_path else None,
        "qualification":"NONE",
        "score_semantics":"local visual keypoint compatibility with geometric coherence; not a probability"
    }
    if calibration_pages is not None and len(calibration_pages) != len(pages):
        raise SystemExit("reference and calibration documents must have the same page count")
    for pno,img in enumerate(pages,1):
        kps,desc=observe_page(img)
        if calibration_pages is None:
            idx=sorted(range(len(kps)), key=lambda i:kps[i].response, reverse=True)[:keep_per_page]
        else:
            ckps,cdesc=observe_page(calibration_pages[pno-1])
            pairs=cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(desc,cdesc,k=2)
            good=[a for a,b in pairs if a.distance < 0.72*b.distance]
            stable=[]
            if len(good)>=8:
                src=np.float32([kps[m.queryIdx].pt for m in good]).reshape(-1,1,2)
                dst=np.float32([ckps[m.trainIdx].pt for m in good]).reshape(-1,1,2)
                _H,mask=cv2.findHomography(src,dst,cv2.RANSAC,5.0)
                if mask is not None:
                    stable=[m.queryIdx for m,ok in zip(good,mask.ravel()) if ok]
            idx=sorted(set(stable), key=lambda i:kps[i].response, reverse=True)[:keep_per_page]
        out["reference"]["pages"].append({
            "page":pno,"width":int(img.shape[1]),"height":int(img.shape[0]),
            "features":[
                {"x":round(kps[i].pt[0]/img.shape[1],6),
                 "y":round(kps[i].pt[1]/img.shape[0],6),
                 "descriptor":bytes(desc[i]).hex()}
                for i in idx
            ]
        })
    return out

def match_page(ref_page, img, cfg):
    k2,d2=observe_page(img)
    feats=ref_page["features"]
    if not feats or len(d2)<2:
        return {"good_matches":0,"inliers":0,"inlier_ratio":0.0}
    d1=np.array([np.frombuffer(bytes.fromhex(f["descriptor"]), dtype=np.uint8) for f in feats], dtype=np.uint8)
    w,h=ref_page["width"],ref_page["height"]
    ref_xy=np.float32([[f["x"]*w,f["y"]*h] for f in feats])
    pairs=cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(d1,d2,k=2)
    good=[a for a,b in pairs if a.distance < cfg["ratio_test"]*b.distance]
    inliers=0
    if len(good)>=8:
        src=np.float32([ref_xy[m.queryIdx] for m in good]).reshape(-1,1,2)
        dst=np.float32([k2[m.trainIdx].pt for m in good]).reshape(-1,1,2)
        _H,mask=cv2.findHomography(src,dst,cv2.RANSAC,cfg["ransac_reproj_px"])
        if mask is not None:
            inliers=int(mask.sum())
    return {"good_matches":len(good),"inliers":inliers,"inlier_ratio":round(inliers/max(1,len(good)),4)}

def match_document(pdf_path: Path, reference):
    pages=render_pdf(pdf_path, reference["observer"]["dpi"])
    mp=reference["matcher"]; policy=reference["decision_policy"]
    details=[]; matched=0
    for i,refp in enumerate(reference["reference"]["pages"]):
        if i>=len(pages):
            d={"page":i+1,"good_matches":0,"inliers":0,"inlier_ratio":0.0,"matched":False}
        else:
            d=match_page(refp,pages[i],mp)
            ok=(d["good_matches"]>=policy["min_good_matches"]
                and d["inliers"]>=policy["min_inliers"]
                and d["inlier_ratio"]>=policy["min_inlier_ratio"])
            d.update({"page":i+1,"matched":ok})
            matched+=int(ok)
        details.append(d)
    ratio=matched/max(1,len(reference["reference"]["pages"]))
    candidate=(len(pages)==reference["reference"]["page_count"]
               and ratio>=policy["min_matching_pages_ratio"])
    return {
        "status":"MATCH_CANDIDATE" if candidate else "UNKNOWN",
        "ulistag_id":reference["ulistag_id"],
        "page_count_observed":len(pages),
        "matching_pages":matched,
        "matching_pages_ratio":round(ratio,4),
        "pages":details,
        "qualification":"NONE",
        "score_semantics":reference["score_semantics"]
    }

def main():
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest="cmd",required=True)
    b=sub.add_parser("build-reference")
    b.add_argument("document",type=Path)
    b.add_argument("--ulistag-id",required=True)
    b.add_argument("--output",type=Path,required=True)
    b.add_argument("--dpi",type=int,default=120)
    b.add_argument("--keep-per-page",type=int,default=100)
    b.add_argument("--calibration-document",type=Path)
    m=sub.add_parser("match")
    m.add_argument("document",type=Path)
    m.add_argument("--reference",type=Path,required=True)
    args=ap.parse_args()
    if args.cmd=="build-reference":
        ref=build_reference(args.document,args.ulistag_id,args.dpi,args.keep_per_page,args.calibration_document)
        args.output.write_text(json.dumps(ref,ensure_ascii=False,indent=2),encoding="utf-8")
        print(json.dumps({"status":"REFERENCE_BUILT","ulistag_id":args.ulistag_id,
                          "pages":ref["reference"]["page_count"],
                          "features_per_page":[len(p["features"]) for p in ref["reference"]["pages"]],
                          "qualification":"NONE"},ensure_ascii=False,indent=2))
    else:
        ref=json.loads(args.reference.read_text(encoding="utf-8"))
        print(json.dumps(match_document(args.document,ref),ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
