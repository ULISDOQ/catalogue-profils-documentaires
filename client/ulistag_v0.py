#!/usr/bin/env python3
"""ULISDOQ ULISTAG v0.1 candidate: deterministic anchor-graph matching + structural extraction."""
import argparse, json, re, unicodedata
from pathlib import Path


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = text.upper().replace("°", " ")
    return " ".join(re.findall(r"[A-Z0-9]+", text))


def phrase_box(words, phrase):
    target = norm(phrase).split()
    tokens = [norm(w["text"]) for w in words]
    for i in range(len(tokens) - len(target) + 1):
        if tokens[i:i + len(target)] == target:
            seg = words[i:i + len(target)]
            return {
                "x0": min(w["x0"] for w in seg),
                "top": min(w["top"] for w in seg),
                "x1": max(w["x1"] for w in seg),
                "bottom": max(w["bottom"] for w in seg),
            }
    return None


def same_line(words, box, tolerance_pt=4):
    cy = (box["top"] + box["bottom"]) / 2
    return sorted(
        [w for w in words if abs(((w["top"] + w["bottom"]) / 2) - cy) <= tolerance_pt],
        key=lambda w: w["x0"],
    )


def load_pdf(path):
    try:
        import pdfplumber
    except ImportError as exc:
        raise SystemExit("pdfplumber is required for this candidate implementation") from exc
    return pdfplumber.open(path)


def observe(pdf_path, reference):
    observed = {"page_count": 0, "nodes": {}}
    with load_pdf(pdf_path) as pdf:
        observed["page_count"] = len(pdf.pages)
        cache = {}
        for node in reference["nodes"]:
            pno = node["page"]
            if pno > len(pdf.pages):
                observed["nodes"][node["id"]] = None
                continue
            page = pdf.pages[pno - 1]
            if pno not in cache:
                cache[pno] = page.extract_words(x_tolerance=2, y_tolerance=2, keep_blank_chars=False)
            box = phrase_box(cache[pno], node["label"])
            if not box:
                observed["nodes"][node["id"]] = None
                continue
            observed["nodes"][node["id"]] = {
                "page": pno,
                "cx": ((box["x0"] + box["x1"]) / 2) / float(page.width),
                "cy": ((box["top"] + box["bottom"]) / 2) / float(page.height),
            }
    return observed


def compare(reference, observed):
    ref_nodes = {n["id"]: n for n in reference["nodes"]}
    node_ok = 0
    node_details = []
    for nid, rn in ref_nodes.items():
        on = observed["nodes"].get(nid)
        if not on:
            node_details.append({"id": nid, "found": False})
            continue
        distance = ((on["cx"] - rn["cx"]) ** 2 + (on["cy"] - rn["cy"]) ** 2) ** 0.5
        geometry_ok = distance <= rn.get("tol", 0.035)
        node_ok += int(geometry_ok)
        node_details.append({"id": nid, "found": True, "geometry_ok": geometry_ok,
                             "distance": round(distance, 6)})
    node_ratio = node_ok / max(1, len(ref_nodes))

    edge_ok = 0
    edge_details = []
    for edge in reference.get("edges", []):
        ra, rb = ref_nodes[edge["a"]], ref_nodes[edge["b"]]
        oa = observed["nodes"].get(edge["a"])
        ob = observed["nodes"].get(edge["b"])
        if not oa or not ob:
            edge_details.append({"a": edge["a"], "b": edge["b"], "tested": False})
            continue
        rdx, rdy = rb["cx"] - ra["cx"], rb["cy"] - ra["cy"]
        odx, ody = ob["cx"] - oa["cx"], ob["cy"] - oa["cy"]
        error = ((odx - rdx) ** 2 + (ody - rdy) ** 2) ** 0.5
        ok = error <= edge.get("tol", 0.04)
        edge_ok += int(ok)
        edge_details.append({"a": edge["a"], "b": edge["b"], "tested": True,
                             "ok": ok, "error": round(error, 6)})
    edge_ratio = edge_ok / max(1, len(reference.get("edges", [])))

    policy = reference["decision_policy"]
    candidate = (
        observed["page_count"] == reference["page_count"]
        and node_ratio >= policy["candidate_min_node_ratio"]
        and edge_ratio >= policy["candidate_min_edge_ratio"]
    )
    return {
        "status": "MATCH_CANDIDATE" if candidate else "UNKNOWN",
        "ulistag_id": reference["ulistag_id"],
        "page_count_observed": observed["page_count"],
        "node_ratio": round(node_ratio, 4),
        "edge_ratio": round(edge_ratio, 4),
        "node_details": node_details,
        "edge_details": edge_details,
        "qualification": "NONE",
        "score_semantics": "deterministic structural compatibility; not a probability",
    }


def extract(pdf_path, profile, evidence_only=False):
    result = {}
    with load_pdf(pdf_path) as pdf:
        cache = {}
        for field in profile["fields"]:
            pno = field["page"]
            page = pdf.pages[pno - 1]
            if pno not in cache:
                cache[pno] = page.extract_words(x_tolerance=2, y_tolerance=2, keep_blank_chars=False)
            words = cache[pno]
            box = phrase_box(words, field["anchor"])
            if not box:
                result[field["name"]] = {"status": "ANCHOR_MISSING"}
                continue
            line = same_line(words, box, field.get("line_tolerance_pt", 4))
            value = None
            if field["strategy"] == "between_anchor_and_token":
                parts = []
                stop = norm(field["stop_token"])
                for word in [w for w in line if w["x0"] >= box["x1"] - 1]:
                    if norm(word["text"]) == stop:
                        break
                    parts.append(word["text"])
                value = " ".join(parts).strip() or None
            elif field["strategy"] == "after_token_same_line":
                token = norm(field["token"])
                candidates = [w for w in line if w["x0"] >= box["x1"] - 1]
                for i, word in enumerate(candidates):
                    if norm(word["text"]) == token and i + 1 < len(candidates):
                        value = candidates[i + 1]["text"]
                        break
            elif field["strategy"] == "right_band_same_line":
                xmin = field.get("x_min_norm", 0.70) * float(page.width)
                rx = re.compile(field["value_regex"])
                for word in line:
                    if word["x0"] >= xmin:
                        match = rx.search(word["text"])
                        if match:
                            value = match.group(1) if match.groups() else match.group(0)
                            break
            item = {"status": "EXTRACTED" if value is not None else "VALUE_NOT_FOUND"}
            if value is not None and not evidence_only:
                item["value"] = value
            result[field["name"]] = item
    return {"status": "EXTRACTED_UNVERIFIED", "profile_id": profile["profile_id"], "fields": result}


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="command", required=True)
    m = sub.add_parser("match")
    m.add_argument("document", type=Path)
    m.add_argument("--reference", type=Path, required=True)
    e = sub.add_parser("extract")
    e.add_argument("document", type=Path)
    e.add_argument("--profile", type=Path, required=True)
    e.add_argument("--evidence-only", action="store_true")
    args = ap.parse_args()

    if args.command == "match":
        reference = json.loads(args.reference.read_text(encoding="utf-8"))
        output = compare(reference, observe(args.document, reference))
    else:
        profile = json.loads(args.profile.read_text(encoding="utf-8"))
        output = extract(args.document, profile, evidence_only=args.evidence_only)
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
