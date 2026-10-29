#!/usr/bin/env python3
"""Generic Linux preflight for ULISDOQ deployment."""
import json, os, platform, shutil, ssl, subprocess, sys

def cmd(args):
    try:
        p=subprocess.run(args,capture_output=True,text=True,timeout=10)
        return p.returncode,(p.stdout or p.stderr).strip()
    except Exception as e:
        return 127,type(e).__name__

checks={}
checks["linux"]={"pass":sys.platform.startswith("linux"),"observed":sys.platform}
checks["arch"]={"pass":platform.machine()=="x86_64","observed":platform.machine(),"qualified":["x86_64"]}
checks["python"]={"pass":platform.python_version().startswith("3.12."),"observed":platform.python_version(),"required":"3.12.x"}
checks["venv_module"]={"pass":True}
try:
    import venv
except Exception as e:
    checks["venv_module"]={"pass":False,"error":type(e).__name__}

for name,binary in [("git","git"),("sha256sum","sha256sum")]:
    path=shutil.which(binary)
    rc,out=cmd([binary,"--version"]) if path else (127,"NOT_FOUND")
    checks[name]={"pass":bool(path) and rc==0,"path":path,"version":out.splitlines()[0] if out else out}

rc,out=cmd([sys.executable,"-m","pip","--version"])
checks["pip"]={"pass":rc==0,"version":out}

checks["ssl_ca"]={"pass":bool(ssl.get_default_verify_paths().cafile or ssl.get_default_verify_paths().capath)}

status="PASS" if all(v.get("pass",False) for v in checks.values()) else "FAIL"
print(json.dumps({
    "status":status,
    "hostname":platform.node(),
    "os":platform.platform(),
    "kernel":platform.release(),
    "arch":platform.machine(),
    "python_executable":sys.executable,
    "checks":checks,
    "qualification":"HOST_PRECHECK_ONLY"
},indent=2))
sys.exit(0 if status=="PASS" else 1)
