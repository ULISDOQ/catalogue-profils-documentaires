#!/usr/bin/env python3
from __future__ import annotations
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys

def run(cmd, cwd=None):
    try:
        p=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,timeout=60)
        return p.returncode,(p.stdout or ""), (p.stderr or "")
    except Exception as exc:
        return 127,"",f"{type(exc).__name__}: {exc}"

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

ap=argparse.ArgumentParser()
ap.add_argument("--repo-root",type=Path,required=True)
ap.add_argument("--profile-root",type=Path,required=True)
args=ap.parse_args()
repo=args.repo_root.resolve()
root=args.profile_root.resolve()
venvs=root/"venvs"

checks={}
def check(name, ok, **data):
    checks[name]={"pass":bool(ok),**data}
    return bool(ok)

def py(env):
    return str(venvs/env/"bin/python")

overall=True

# Host and source
overall &= check("host_linux",sys.platform.startswith("linux"),observed=sys.platform)
overall &= check("arch_x86_64",platform.machine()=="x86_64",observed=platform.machine())
v=tuple(map(int,platform.python_version_tuple()))
overall &= check("python_minimum",v >= (3,12,3),observed=platform.python_version(),minimum="3.12.3")

rc,out,err=run(["git","-C",str(repo),"rev-parse","HEAD"])
head=out.strip() if rc==0 else "UNKNOWN"
overall &= check("source_git",rc==0,commit=head)

rc,out,err=run(["git","-C",str(repo),"status","--porcelain"])
overall &= check("source_clean",rc==0 and not out.strip(),dirty=out.strip())

# Core client TAG test
rc,out,err=run([py("core"),"test_tag_candidate.py"],cwd=repo/"client")
overall &= check("client_tag_candidate",rc==0,stdout=out[-2000:],stderr=err[-2000:])

# Anchor graph
code="import pdfplumber; print(pdfplumber.__version__)"
rc,out,err=run([py("anchor_graph"),"-c",code])
anchor_ver=out.strip()
overall &= check("anchor_graph_pdfplumber",rc==0 and anchor_ver=="0.11.10",observed=anchor_ver,expected="0.11.10")
rc,out,err=run([py("anchor_graph"),str(repo/"ULISTAG/matchers/anchor_graph/ulistag_v0.py"),"--help"])
overall &= check("anchor_graph_cli",rc==0,stderr=err[-1000:])

# Visual keypoints: versions + functional primitives
visual_code=r"""
import json, cv2, fitz, numpy as np
from importlib.metadata import version
img=np.zeros((320,320),dtype=np.uint8)
cv2.rectangle(img,(30,30),(290,290),255,3)
cv2.putText(img,'ULISDOQ',(55,160),cv2.FONT_HERSHEY_SIMPLEX,1.0,255,2)
orb=cv2.ORB_create(nfeatures=500)
kp,d=orb.detectAndCompute(img,None)
shift=np.roll(img,4,axis=1)
kp2,d2=orb.detectAndCompute(shift,None)
pairs=cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(d,d2,k=2)
good=[a for a,b in pairs if a.distance < 0.8*b.distance]
homography=False
if len(good)>=8:
    src=np.float32([kp[m.queryIdx].pt for m in good]).reshape(-1,1,2)
    dst=np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1,1,2)
    H,mask=cv2.findHomography(src,dst,cv2.RANSAC,5.0)
    homography=mask is not None and int(mask.sum())>=8
doc=fitz.open(); page=doc.new_page(width=200,height=200); page.insert_text((20,80),'ULISDOQ')
pix=page.get_pixmap(colorspace=fitz.csGRAY,alpha=False)
print(json.dumps({
 'opencv_dist':version('opencv-python-headless'),
 'cv2':cv2.__version__,
 'numpy':version('numpy'),
 'pymupdf':version('PyMuPDF'),
 'keypoints':len(kp),
 'good_matches':len(good),
 'homography':homography,
 'render':bool(pix.samples)
}))
"""
rc,out,err=run([py("visual_keypoints"),"-c",visual_code])
try: visual=json.loads(out.strip()) if rc==0 else {}
except Exception: visual={}
visual_ok=(rc==0 and visual.get("opencv_dist")=="4.13.0.92" and
           visual.get("numpy")=="2.3.5" and visual.get("pymupdf")=="1.26.7" and
           visual.get("homography") and visual.get("render"))
overall &= check("visual_keypoints",visual_ok,observed=visual,stderr=err[-1000:])

# invoice2data client environment
invoice_code="from importlib.metadata import version; import invoice2data; print(version('invoice2data'))"
rc,out,err=run([py("invoice2data"),"-c",invoice_code])
invoice_ver=out.strip()
overall &= check("invoice2data_import",rc==0 and invoice_ver=="0.4.5",observed=invoice_ver,expected="0.4.5")
rc,out,err=run([py("invoice2data"),str(repo/"client/extract.py"),"--help"])
overall &= check("invoice2data_client_cli",rc==0,stderr=err[-1000:])

# OCR system capability and language data
tess=shutil.which("tesseract")
rc,out,err=run(["tesseract","--version"]) if tess else (127,"","NOT_FOUND")
first=(out or err).splitlines()[0] if (out or err) else "NOT_FOUND"
overall &= check("tesseract_present",rc==0,path=tess,version=first)
rc,out,err=run(["tesseract","--list-langs"]) if tess else (127,"","NOT_FOUND")
langs=set((out+"
"+err).split())
overall &= check("tesseract_languages",rc==0 and {"fra","eng"}.issubset(langs),observed=sorted(langs))

# Semantic schema validation
schema_path=repo/"experiments/impots-finances/GED-02/extraction/semantic_extraction_schema_v0_1.json"
semantic_code=f"""
import json
from jsonschema import validate
schema=json.load(open({str(schema_path)!r},encoding='utf-8'))
sample={{'document_profile_id':'TEST','specimen_id':'TEST','fields':[]}}
validate(sample,schema)
from importlib.metadata import version
print(version('jsonschema'))
"""
rc,out,err=run([py("semantic_validation"),"-c",semantic_code])
sem_ver=out.strip()
overall &= check("semantic_schema_validation",rc==0 and sem_ver=="4.25.1",observed=sem_ver,stderr=err[-1000:])

# System reader utility
poppler=shutil.which("pdftotext")
rc,out,err=run(["pdftotext","-v"]) if poppler else (127,"","NOT_FOUND")
overall &= check("poppler_pdftotext",rc==0,path=poppler,version=(err or out).splitlines()[0] if (err or out) else "")

# Locks
locks={}
for env in ["core","anchor_graph","visual_keypoints","invoice2data","semantic_validation"]:
    p=root/"evidence"/f"lock-{env}.txt"
    locks[env]={"exists":p.exists(),"sha256":sha256(p) if p.exists() else None}
    overall &= check("lock_"+env,p.exists(),sha256=locks[env]["sha256"])

# GPU is informational only in v0.1
gpu={"required":False}
nvidia=shutil.which("nvidia-smi")
if nvidia:
    rc,out,err=run(["nvidia-smi","--query-gpu=name,driver_version,memory.total","--format=csv,noheader"])
    gpu.update({"present":rc==0,"details":out.strip() if rc==0 else err.strip()})
else:
    gpu.update({"present":False})

result={
  "profile_id":"ULISDOQ-COMPLETE-UBUNTU-V0.1",
  "status":"PASS" if overall else "FAIL",
  "qualification":"CAPABILITY_PROFILE_VERIFICATION_ONLY",
  "source_commit":head,
  "host":{
    "hostname":platform.node(),
    "platform":platform.platform(),
    "kernel":platform.release(),
    "arch":platform.machine(),
    "python":platform.python_version()
  },
  "checks":checks,
  "locks":locks,
  "gpu":gpu,
  "notes":[
    "PASS does not qualify a document profile or ULISTAG method for production.",
    "CUDA/GPU is not a dependency of the declared v0.1 capability profile."
  ]
}
print(json.dumps(result,ensure_ascii=False,indent=2))
sys.exit(0 if overall else 1)
