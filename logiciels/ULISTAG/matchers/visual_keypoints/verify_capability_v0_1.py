#!/usr/bin/env python3
"""PCIA capability verification for ULISTAG visual-keypoints v0.1."""
import json
import platform
import re
import subprocess
import sys

EXPECTED = {
    "python": "3.12.3",
    "opencv": "4.13.0",
    "numpy": "2.3.5",
    "pymupdf": "1.26.7",
    "tesseract": "5.3.4",
}

result = {"method_id": "ULISTAG-VISUAL-KEYPOINTS-ORB-HAMMING-RANSAC", "checks": {}}

def check(name, observed, expected, ok=None):
    if ok is None:
        ok = observed == expected
    result["checks"][name] = {"observed": observed, "expected": expected, "pass": bool(ok)}
    return bool(ok)

all_ok = True
all_ok &= check("python_exact_version", platform.python_version(), EXPECTED["python"])

try:
    import cv2
    all_ok &= check("opencv_version", cv2.__version__, EXPECTED["opencv"])
except Exception as e:
    result["checks"]["opencv_version"] = {"pass": False, "error": type(e).__name__}
    all_ok = False
    cv2 = None

try:
    import numpy as np
    all_ok &= check("numpy_version", np.__version__, EXPECTED["numpy"])
except Exception as e:
    result["checks"]["numpy_version"] = {"pass": False, "error": type(e).__name__}
    all_ok = False
    np = None

try:
    import fitz
    observed = getattr(fitz, "VersionBind", "UNKNOWN")
    all_ok &= check("pymupdf_version", observed, EXPECTED["pymupdf"])
except Exception as e:
    result["checks"]["pymupdf_version"] = {"pass": False, "error": type(e).__name__}
    all_ok = False
    fitz = None

if cv2 is not None and np is not None:
    try:
        img = np.zeros((400, 400), dtype=np.uint8)
        cv2.rectangle(img, (50, 50), (350, 350), 255, 3)
        cv2.line(img, (50, 200), (350, 200), 255, 2)
        cv2.putText(img, "ULISDOQ", (80, 130), cv2.FONT_HERSHEY_SIMPLEX, 1.2, 255, 2)
        orb = cv2.ORB_create(nfeatures=500)
        kp, desc = orb.detectAndCompute(img, None)
        ok = desc is not None and len(kp) >= 8
        result["checks"]["orb_feature_detection"] = {"pass": ok, "keypoints": len(kp)}
        all_ok &= ok

        shifted = np.roll(img, 5, axis=1)
        kp2, desc2 = orb.detectAndCompute(shifted, None)
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
        pairs = matcher.knnMatch(desc, desc2, k=2)
        good = [a for a, b in pairs if a.distance < 0.8 * b.distance]
        ok_match = len(good) >= 8
        result["checks"]["hamming_matching"] = {"pass": ok_match, "good_matches": len(good)}
        all_ok &= ok_match

        ok_h = False
        if ok_match:
            src = np.float32([kp[m.queryIdx].pt for m in good]).reshape(-1,1,2)
            dst = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1,1,2)
            _H, mask = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
            ok_h = mask is not None and int(mask.sum()) >= 8
        result["checks"]["ransac_homography"] = {"pass": ok_h}
        all_ok &= ok_h
    except Exception as e:
        result["checks"]["opencv_capabilities"] = {"pass": False, "error": type(e).__name__}
        all_ok = False

if fitz is not None:
    try:
        doc = fitz.open()
        page = doc.new_page(width=300, height=300)
        page.insert_text((50, 100), "ULISDOQ")
        pix = page.get_pixmap(matrix=fitz.Matrix(1, 1), colorspace=fitz.csGRAY, alpha=False)
        ok = pix.width == 300 and pix.height == 300 and len(pix.samples) > 0
        result["checks"]["pymupdf_render"] = {"pass": ok, "width": pix.width, "height": pix.height}
        all_ok &= ok
        doc.close()
    except Exception as e:
        result["checks"]["pymupdf_render"] = {"pass": False, "error": type(e).__name__}
        all_ok = False

try:
    cp = subprocess.run(["tesseract", "--version"], capture_output=True, text=True, timeout=10)
    line = (cp.stdout or cp.stderr).splitlines()[0] if (cp.stdout or cp.stderr) else ""
    m = re.search(r"(\d+\.\d+\.\d+)", line)
    observed = m.group(1) if m else "UNKNOWN"
    all_ok &= check("tesseract_exact_version", observed, EXPECTED["tesseract"])
except Exception as e:
    result["checks"]["tesseract_exact_version"] = {"pass": False, "error": type(e).__name__}
    all_ok = False

result["status"] = "PASS" if all_ok else "FAIL"
result["qualification"] = "CAPABILITY_VERIFICATION_ONLY"
print(json.dumps(result, ensure_ascii=False, indent=2))
sys.exit(0 if all_ok else 1)
