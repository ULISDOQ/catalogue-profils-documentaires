#!/usr/bin/env python3
from __future__ import annotations
import importlib, json, platform, re, shutil, subprocess, sys

def run(args):
    try:
        p=subprocess.run(args,capture_output=True,text=True,timeout=20)
        return p.returncode,(p.stdout or p.stderr).strip()
    except Exception as e:
        return 127,type(e).__name__

checks={}
def add(name, ok, **extra):
    checks[name]={"pass":bool(ok),**extra}
    return bool(ok)

cpu_ok=True
cpu_ok &= add("linux",sys.platform.startswith("linux"),observed=sys.platform)
cpu_ok &= add("x86_64",platform.machine()=="x86_64",observed=platform.machine())
cpu_ok &= add("python_minimum",tuple(map(int,platform.python_version_tuple())) >= (3,12,3),
              observed=platform.python_version(),minimum="3.12.3")

os_release={}
try:
    with open("/etc/os-release",encoding="utf-8") as f:
        for line in f:
            if "=" in line:
                k,v=line.rstrip().split("=",1); os_release[k]=v.strip('"')
except Exception:
    pass
ubuntu_ok=os_release.get("ID")=="ubuntu"
cpu_ok &= add("ubuntu",ubuntu_ok,observed=os_release.get("PRETTY_NAME","UNKNOWN"))

for name,args in {
    "git":["git","--version"],
    "curl":["curl","--version"],
    "jq":["jq","--version"],
    "pdftotext":["pdftotext","-v"],
    "pdftoppm":["pdftoppm","-v"],
    "qpdf":["qpdf","--version"],
    "ghostscript":["gs","--version"],
    "tesseract":["tesseract","--version"],
}.items():
    path=shutil.which(args[0]); rc,out=run(args) if path else (127,"NOT_FOUND")
    cpu_ok &= add(name,bool(path) and rc==0,path=path,version=(out.splitlines()[0] if out else out))

mods={
    "pydantic":"pydantic","jsonschema":"jsonschema","yaml":"yaml","requests":"requests",
    "httpx":"httpx","pypdf":"pypdf","pdfplumber":"pdfplumber","pymupdf":"fitz",
    "pdf2image":"pdf2image","PIL":"PIL","numpy":"numpy","scipy":"scipy","opencv":"cv2",
    "skimage":"skimage","pytesseract":"pytesseract","rapidfuzz":"rapidfuzz",
    "pandas":"pandas","openpyxl":"openpyxl","docx":"docx","odf":"odf",
    "pyzbar":"pyzbar","invoice2data":"invoice2data","pytest":"pytest",
    "torch":"torch","torchvision":"torchvision","transformers":"transformers",
    "onnxruntime":"onnxruntime"
}
versions={}
for label,name in mods.items():
    try:
        m=importlib.import_module(name)
        versions[label]=str(getattr(m,"__version__",getattr(m,"VERSION","UNKNOWN")))
        cpu_ok &= add("python_"+label,True,version=versions[label])
    except Exception as e:
        cpu_ok &= add("python_"+label,False,error=type(e).__name__)

try:
    import cv2, numpy as np
    img=np.zeros((400,400),dtype=np.uint8)
    cv2.rectangle(img,(40,40),(360,360),255,3)
    cv2.putText(img,"ULISDOQ",(70,200),cv2.FONT_HERSHEY_SIMPLEX,1.2,255,2)
    kp,desc=cv2.ORB_create(nfeatures=500).detectAndCompute(img,None)
    cpu_ok &= add("functional_orb",desc is not None and len(kp)>=8,keypoints=len(kp))
except Exception as e:
    cpu_ok &= add("functional_orb",False,error=type(e).__name__)

gpu={"required_for_full_gpu_profile":True}
nvidia=shutil.which("nvidia-smi")
if nvidia:
    rc,out=run(["nvidia-smi","--query-gpu=name,driver_version,memory.total","--format=csv,noheader"])
    gpu["nvidia_smi"]={"pass":rc==0,"output":out}
    _,full=run(["nvidia-smi"])
    m=re.search(r"CUDA Version:\s*([0-9.]+)",full)
    gpu["cuda_driver_capability"]=m.group(1) if m else "UNKNOWN"
else:
    gpu["nvidia_smi"]={"pass":False,"output":"NOT_FOUND"}
    gpu["cuda_driver_capability"]="UNKNOWN"

try:
    import torch
    gpu["torch_cuda_available"]=bool(torch.cuda.is_available())
    gpu["torch_cuda_runtime"]=torch.version.cuda
    if torch.cuda.is_available():
        gpu["device_name"]=torch.cuda.get_device_name(0)
        gpu["device_capability"]=list(torch.cuda.get_device_capability(0))
        gpu["vram_bytes"]=torch.cuda.get_device_properties(0).total_memory
except Exception as e:
    gpu["torch_error"]=type(e).__name__

gpu_ok=bool(gpu.get("nvidia_smi",{}).get("pass") and gpu.get("torch_cuda_available"))

print(json.dumps({
  "stack_id":"ULISDOQ-FULL-UBUNTU-PHASE1-V0.1",
  "status_cpu_document_stack":"PASS" if cpu_ok else "FAIL",
  "status_gpu_stack":"PASS" if gpu_ok else "FAIL",
  "hostname":platform.node(),
  "os_release":os_release,
  "kernel":platform.release(),
  "arch":platform.machine(),
  "python_executable":sys.executable,
  "python_version":platform.python_version(),
  "python_modules":versions,
  "checks":checks,
  "gpu":gpu,
  "qualification":"CAPABILITY_VERIFICATION_ONLY"
},ensure_ascii=False,indent=2))
sys.exit(0 if cpu_ok else 1)
