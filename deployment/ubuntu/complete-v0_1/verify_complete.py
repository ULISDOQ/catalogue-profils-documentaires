#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile


def run(cmd, cwd=None, timeout=90):
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout or "", p.stderr or ""
    except Exception as exc:
        return 127, "", f"{type(exc).__name__}: {exc}"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


ap = argparse.ArgumentParser()
ap.add_argument("--repo-root", type=Path, required=True)
ap.add_argument("--profile-root", type=Path, required=True)
ap.add_argument("--env", action="append", default=[], help="NAME=VENV_PATH")
args = ap.parse_args()

repo = args.repo_root.resolve()
root = args.profile_root.resolve()

envs = {}
for item in args.env:
    if "=" not in item:
        ap.error("--env requires NAME=PATH")
    name, value = item.split("=", 1)
    envs[name] = Path(value).resolve()

required_envs = {"core", "anchor_graph", "visual_keypoints", "invoice2data", "semantic_validation", "profile_extraction"}
missing_envs = sorted(required_envs - set(envs))

checks = {}


def check(name, ok, **data):
    checks[name] = {"pass": bool(ok), **data}
    return bool(ok)


def py(name):
    return str(envs[name] / "bin/python")


overall = True
overall &= check("environment_bindings_complete", not missing_envs, missing=missing_envs)

# Host and source.
overall &= check("host_linux", sys.platform.startswith("linux"), observed=sys.platform)
overall &= check("arch_x86_64", platform.machine() == "x86_64", observed=platform.machine())
v = tuple(map(int, platform.python_version_tuple()))
overall &= check(
    "python_minimum",
    v >= (3, 12, 3),
    observed=platform.python_version(),
    minimum="3.12.3",
)

rc, out, err = run(["git", "-C", str(repo), "rev-parse", "HEAD"])
head = out.strip() if rc == 0 else "UNKNOWN"
overall &= check("source_git", rc == 0, commit=head)

rc, out, err = run(["git", "-C", str(repo), "status", "--porcelain"])
overall &= check("source_clean", rc == 0 and not out.strip(), dirty=out.strip())

# Verify every explicit environment binding before using it.
for name in sorted(required_envs):
    exe = envs.get(name, Path("/missing")) / "bin/python"
    ok = exe.is_file() and exe.stat().st_mode & 0o111 != 0
    overall &= check(f"env_{name}_python", ok, path=str(exe))

if missing_envs:
    result = {
        "profile_id": "ULISDOQ-COMPLETE-UBUNTU-V0.1",
        "status": "FAIL",
        "qualification": "CAPABILITY_PROFILE_VERIFICATION_ONLY",
        "source_commit": head,
        "checks": checks,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(1)

# Profile-extraction environment: version and import sanity.
rc, out, err = run(
    [
        py("profile_extraction"),
        "-c",
        "from importlib.metadata import version; import fitz, jsonschema; "
        "print(version('PyMuPDF') + '|' + version('jsonschema'))",
    ]
)
profile_extract_versions = out.strip()
overall &= check(
    "profile_extraction_dependencies",
    rc == 0 and profile_extract_versions == "1.26.7|4.25.1",
    observed=profile_extract_versions,
    expected="1.26.7|4.25.1",
    stderr=err[-1000:],
)

# Core client TAG functional test.
rc, out, err = run([py("core"), "test_tag_candidate.py"], cwd=repo / "client")
overall &= check("client_tag_candidate", rc == 0, stdout=out[-2000:], stderr=err[-2000:])

# Versions / imports.
rc, out, err = run([py("anchor_graph"), "-c", "import pdfplumber; print(pdfplumber.__version__)"])
anchor_ver = out.strip()
overall &= check(
    "anchor_graph_pdfplumber",
    rc == 0 and anchor_ver == "0.11.10",
    observed=anchor_ver,
    expected="0.11.10",
)

visual_code = r"""
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
 'numpy':version('numpy'),
 'pymupdf':version('PyMuPDF'),
 'keypoints':len(kp),
 'good_matches':len(good),
 'homography':homography,
 'render':bool(pix.samples)
}))
"""
rc, out, err = run([py("visual_keypoints"), "-c", visual_code])
try:
    visual = json.loads(out.strip()) if rc == 0 else {}
except Exception:
    visual = {}
visual_ok = (
    rc == 0
    and visual.get("opencv_dist") == "4.13.0.92"
    and visual.get("numpy") == "2.3.5"
    and visual.get("pymupdf") == "1.26.7"
    and visual.get("homography")
    and visual.get("render")
)
overall &= check("visual_keypoints", visual_ok, observed=visual, stderr=err[-1000:])

rc, out, err = run(
    [
        py("invoice2data"),
        "-c",
        "from importlib.metadata import version; import invoice2data; print(version('invoice2data'))",
    ]
)
invoice_ver = out.strip()
overall &= check(
    "invoice2data_import",
    rc == 0 and invoice_ver == "0.4.5",
    observed=invoice_ver,
    expected="0.4.5",
)

# System OCR presence + language data.
tess = shutil.which("tesseract")
rc, out, err = run(["tesseract", "--version"]) if tess else (127, "", "NOT_FOUND")
first = (out or err).splitlines()[0] if (out or err) else "NOT_FOUND"
overall &= check("tesseract_present", rc == 0, path=tess, version=first)
rc, out, err = run(["tesseract", "--list-langs"]) if tess else (127, "", "NOT_FOUND")
langs = set((out + "\n" + err).split())
overall &= check(
    "tesseract_languages",
    rc == 0 and {"fra", "eng"}.issubset(langs),
    observed=sorted(langs),
)

# System PDF reader.
poppler = shutil.which("pdftotext")
rc, out, err = run(["pdftotext", "-v"]) if poppler else (127, "", "NOT_FOUND")
overall &= check(
    "poppler_pdftotext",
    rc == 0,
    path=poppler,
    version=(err or out).splitlines()[0] if (err or out) else "",
)

# Semantic validation.
schema_path = repo / "experiments/impots-finances/GED-02/extraction/semantic_extraction_schema_v0_1.json"
semantic_code = f"""
import json
from jsonschema import validate
schema=json.load(open({str(schema_path)!r},encoding='utf-8'))
sample={{'document_profile_id':'TEST','specimen_id':'TEST','fields':[]}}
validate(sample,schema)
from importlib.metadata import version
print(version('jsonschema'))
"""
rc, out, err = run([py("semantic_validation"), "-c", semantic_code])
sem_ver = out.strip()
overall &= check(
    "semantic_schema_validation",
    rc == 0 and sem_ver == "4.25.1",
    observed=sem_ver,
    stderr=err[-1000:],
)

# Functional probes use temporary synthetic material only.
with tempfile.TemporaryDirectory(prefix="ulisdoq-verify-") as td:
    td = Path(td)
    pdf = td / "probe.pdf"
    png = td / "probe.png"

    # Generate a deterministic synthetic PDF + PNG with the visual environment.
    generator = f"""
import fitz
doc=fitz.open()
p=doc.new_page(width=595,height=842)
p.insert_text((72,100),'ULISDOQ FACTURE TEST',fontsize=18)
p.insert_text((72,150),'FACTURE N TEST-001 DU 01/01/2026',fontsize=14)
p.insert_text((72,200),'Montant facture (EUR) 42,00',fontsize=14)
doc.save({str(pdf)!r})
page=doc[0]
pix=page.get_pixmap(matrix=fitz.Matrix(2,2),colorspace=fitz.csGRAY,alpha=False)
pix.save({str(png)!r})
"""
    rc, out, err = run([py("visual_keypoints"), "-c", generator])
    overall &= check("fixture_generation", rc == 0 and pdf.exists() and png.exists(), stderr=err[-1000:])

    # Minimal functional OCR: image -> text, not only tesseract --version.
    ocr_txt = td / "ocr-probe"
    rc, out, err = run(["tesseract", str(png), str(ocr_txt), "-l", "eng", "--psm", "6"]) if tess else (127, "", "NOT_FOUND")
    ocr_file = Path(str(ocr_txt) + ".txt")
    ocr_value = ocr_file.read_text(encoding="utf-8", errors="replace") if ocr_file.exists() else ""
    ocr_ok = rc == 0 and "ULISDOQ" in ocr_value.upper()
    overall &= check("functional_ocr", ocr_ok, observed=ocr_value[:500], stderr=err[-1000:])

    # Minimal functional anchor-graph: create observed anchors, turn them into a reference,
    # then execute the real matcher and require MATCH_CANDIDATE.
    anchor_script = repo / "ULISTAG/matchers/anchor_graph/ulistag_v0.py"
    anchor_probe = f"""
import importlib.util, json
from pathlib import Path
spec=importlib.util.spec_from_file_location('ag',{str(anchor_script)!r})
ag=importlib.util.module_from_spec(spec); spec.loader.exec_module(ag)
pdf=Path({str(pdf)!r})
seed={{'nodes':[
 {{'id':'TITLE','page':1,'label':'ULISDOQ FACTURE TEST'}},
 {{'id':'NUMBER','page':1,'label':'FACTURE N'}}
]}}
obs=ag.observe(pdf,seed)
nodes=[]
for item in seed['nodes']:
    point=obs['nodes'][item['id']]
    if point is None:
        raise SystemExit('anchor missing: '+item['id'])
    nodes.append({{**item,'cx':point['cx'],'cy':point['cy'],'tol':0.02}})
ref={{
 'ulistag_id':'VERIFY-ANCHOR-GRAPH',
 'page_count':1,
 'nodes':nodes,
 'edges':[{{'a':'TITLE','b':'NUMBER','tol':0.03}}],
 'decision_policy':{{'candidate_min_node_ratio':1.0,'candidate_min_edge_ratio':1.0}}
}}
result=ag.compare(ref,ag.observe(pdf,ref))
print(json.dumps(result))
raise SystemExit(0 if result['status']=='MATCH_CANDIDATE' else 1)
"""
    rc, out, err = run([py("anchor_graph"), "-c", anchor_probe])
    try:
        anchor_result = json.loads(out.strip()) if rc == 0 else {}
    except Exception:
        anchor_result = {}
    overall &= check(
        "functional_anchor_graph",
        rc == 0 and anchor_result.get("status") == "MATCH_CANDIDATE",
        observed=anchor_result,
        stderr=err[-1000:],
    )

    # Minimal functional invoice extraction: real client + real invoice2data engine + pdftotext reader.
    template_dir = td / "templates"
    template_dir.mkdir()
    template = template_dir / "probe.yml"
    template.write_text(
        """issuer: ULISDOQ-VERIFY\nkeywords:\n  - 'ULISDOQ FACTURE TEST'\nfields:\n  invoice_number: 'FACTURE\\s+N\\s+(TEST-[0-9]+)'\n  date: 'DU\\s+(\\d{2}/\\d{2}/\\d{4})'\n  amount: 'Montant\\s+facture\\s+\\(EUR\\)\\s+(\\d+[,.]\\d{2})'\nrequired_fields:\n  - invoice_number\n  - date\n  - amount\noptions:\n  currency: EUR\n  decimal_separator: ','\n  date_formats:\n    - '%d/%m/%Y'\n""",
        encoding="utf-8",
    )
    rc, out, err = run(
        [
            py("invoice2data"),
            str(repo / "client/extract.py"),
            str(pdf),
            "--templates",
            str(template_dir),
            "--reader",
            "pdftotext",
        ],
        timeout=120,
    )
    try:
        extraction = json.loads(out.strip()) if out.strip() else {}
    except Exception:
        extraction = {}
    data = extraction.get("data") or {}
    try:
        amount_ok = abs(float(str(data.get("amount", "")).replace(",", ".")) - 42.0) < 1e-9
    except (TypeError, ValueError):
        amount_ok = False
    extraction_ok = (
        rc == 0
        and extraction.get("status") == "EXTRACTED_UNVERIFIED"
        and str(data.get("invoice_number", "")) == "TEST-001"
        and amount_ok
    )
    overall &= check(
        "functional_invoice_extraction",
        extraction_ok,
        status=extraction.get("status"),
        fields=sorted(data.keys()) if isinstance(data, dict) else [],
        stderr=err[-1500:],
    )

# Lock/evidence integrity. For attached environments, a generated canonical lock may not yet exist;
# record their live freeze digest as evidence instead of pretending they were created by this profile.
locks = {}
for name in sorted(required_envs):
    lock = root / "evidence" / f"lock-{name}.txt"
    if lock.exists():
        locks[name] = {"source": "profile_lock", "sha256": sha256(lock)}
        overall &= check(f"lock_{name}", True, sha256=locks[name]["sha256"])
    else:
        rc, out, err = run([py(name), "-m", "pip", "freeze"])
        live_sha = hashlib.sha256(out.encode("utf-8")).hexdigest() if rc == 0 else None
        locks[name] = {"source": "attached_live_freeze", "sha256": live_sha}
        overall &= check(
            f"lock_{name}",
            rc == 0,
            source="attached_live_freeze",
            sha256=live_sha,
            stderr=err[-500:],
        )

# GPU/CUDA are informational only: no declared v0.1 capability depends on them.
gpu = {"required": False}
nvidia = shutil.which("nvidia-smi")
if nvidia:
    rc, out, err = run(
        ["nvidia-smi", "--query-gpu=name,driver_version,memory.total", "--format=csv,noheader"]
    )
    gpu.update({"present": rc == 0, "details": out.strip() if rc == 0 else err.strip()})
else:
    gpu.update({"present": False})

result = {
    "profile_id": "ULISDOQ-COMPLETE-UBUNTU-V0.1",
    "status": "PASS" if overall else "FAIL",
    "qualification": "CAPABILITY_PROFILE_VERIFICATION_ONLY",
    "source_commit": head,
    "environment_bindings": {name: str(path) for name, path in sorted(envs.items())},
    "host": {
        "hostname": platform.node(),
        "platform": platform.platform(),
        "kernel": platform.release(),
        "arch": platform.machine(),
        "python": platform.python_version(),
    },
    "checks": checks,
    "locks": locks,
    "gpu": gpu,
    "reproducibility_limits": [
        "PCIA complete profile has not yet been runtime-qualified.",
        "Attached environments are accepted only after this global battery passes; their live freeze is evidence, not a canonical lock.",
        "APT repository state can change; exact resolved system package versions must be recorded during target qualification.",
        "Ubuntu/Python versions newer than a tested combination are not assumed compatible.",
        "No CUDA/GPU dependency is declared in v0.1.",
    ],
}
print(json.dumps(result, ensure_ascii=False, indent=2))
sys.exit(0 if overall else 1)
