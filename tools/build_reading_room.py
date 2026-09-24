#!/usr/bin/env python3
"""Build reading_room/index.html — the Reading Room artifact. Authority C.

Inlines the page data, the browser engine and the UI into reading_room/shell.html.
Everything on the page comes from the published build (corpus/*.json), the data
files (data/*.yaml), the diachrony tables and the verifier. **Nothing sealed is read
into the page.** The sealed key is read here for one purpose only: to build the list
of strings that must not appear in the page, and the page is refused if one does.

    python3 -m hel.corpus && python3 tools/build_reading_room.py
"""
from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from hel import __version__, diachrony, export, field  # noqa: E402

RR = ROOT / "reading_room"
SEED = 1908


def load_yaml(name):
    return yaml.safe_load((ROOT / "data" / name).read_text(encoding="utf-8"))


def formulae():
    out = []
    for f in load_yaml("formulae.yaml")["formulae"]:
        f = dict(f)
        f["chicago"] = diachrony.recite(f["text"], "chicago")
        f["second"] = diachrony.recite(f["text"], "second")
        out.append(f)
    return out


def d1():
    rows = diachrony.d1_table()
    n08, n88, total = diachrony.coda_count_1908()
    return {"rows": rows, "irregular": {k: list(v) for k, v in diachrony.IRREGULAR.items()}, "coda": [n08, n88, total]}


def d2():
    return {"rows": diachrony.d2_table(), "rootlike": sorted(diachrony.ROOTLIKE),
            "reconstruction": diachrony.RECONSTRUCTION}


def resolve_featured(cat, featured):
    """Match each "start here" note to its accession (numbers are assigned by the 1949
    renumbering, so they are looked up, never assumed)."""
    out, order = {}, []
    for f in featured:
        m = f["match"]
        hits = [e for e in cat
                if all((" | ".join(s["translit"] for s in e["segments"]) if k == "translit" else e.get(k)) == v
                       for k, v in m.items())]
        if len(hits) != 1:
            raise SystemExit(f"featured note {f['title']!r} matches {len(hits)} accessions")
        ref = hits[0]["ref"]
        out[ref] = {"title": f["title"], "body": f["body"]}
        order.append(ref)
    return out, order


def claims(figs):
    try:
        from hel import verify
    except ImportError:
        return []
    return verify.claims(figs)


def metrics_subset() -> dict:
    from hel import verify
    M = verify.metrics()
    return {k: M[k] for k in ("root_mean_syllables", "root_coda_final_share", "ch1_intact_with_ar",
                              "iii_share_of_hapax", "functional_one_sequence_share", "analyzable_core")}


def sealed_needles() -> dict:
    """Strings drawn from the sealed key that must never appear in the page."""
    key = yaml.safe_load((ROOT / "sealed" / "key.yaml").read_text(encoding="utf-8"))
    truth = json.loads((ROOT / "sealed" / "truth.json").read_text(encoding="utf-8"))
    T = key["TRUTH"]
    needles = {}
    for form, d in T["roots"].items():
        needles[d["def"]] = f"definition of {form}"
        if "_" in d["feature"]:
            needles[d["feature"]] = f"feature name of {form}"
    for d in T["disputes"]:
        for part in (d.get("verdict", ""), d.get("consequence", "")):
            for s in str(part).split(". "):
                if len(s) >= 28:
                    needles[s.strip()] = f"verdict on {d['id']}"
    for e in key["WITHHOLDING"]["entries"]:
        if len(str(e.get("exists", ""))) >= 20:
            needles[e["exists"]] = f"withheld: {e['gap']}"
    for f, (a, c) in truth.get("noncore_roots", {}).items():
        needles[f"{a}&{c}"] = f"compound of {f}"
    needles["hand_composed"] = "the sealed register entry of CSC-1146"
    needles["recognition by the third return"] = "the sealed register entry of CSC-1146"
    needles["427 days"] = "the sealed magnitude of the Quiet Sixteen displacement"
    return needles


def main():
    cat = json.loads((ROOT / "corpus" / "csc.json").read_text(encoding="utf-8"))
    figs = json.loads((ROOT / "corpus" / "figures.json").read_text(encoding="utf-8"))
    reg = json.loads((ROOT / "corpus" / "register.json").read_text(encoding="utf-8"))["units"]
    inventory = json.loads((RR / "inventory.json").read_text(encoding="utf-8"))
    # the Common Recitation and the Second branch's irregulars, straight from the laws
    common = {"common": diachrony.COMMON,
              "second_irregular": {k: v[0] for k, v in diachrony.SECOND_IRREGULAR.items()}}
    (RR / "common.json").write_text(json.dumps(common, ensure_ascii=False), encoding="utf-8")
    fe = field.load()
    problems = field.validate(fe, {u["form"] for u in reg})
    if problems:
        raise SystemExit("field English does not validate:\n  " + "\n  ".join(problems))
    featured = load_yaml("featured.yaml")
    feat, order = resolve_featured(cat, featured["featured"])
    data = {
        "meta": {"version": __version__, "seed": SEED, "built": datetime.date.today().isoformat(),
                 "start": order[0], "featured_order": order},
        "inventory": inventory,
        "register": reg,
        "common": common,
        "entries": cat,
        "figures": figs,
        "featured": feat,
        "locus_names": featured.get("loci", {}),
        "formulae": formulae(),
        "d1": d1(),
        "d2": d2(),
        "field": {k: fe[k] for k in ("name", "crews_call_it", "style_manual_calls_it", "loans",
                                      "euphemism_cycle", "shibboleths", "proverbs", "naming")},
        "naming_pools": {"shapes": field.SHAPES, "intervals": field.INTERVALS, "quiet": field.QUIET,
                         "numbers": field.NUMBERS,
                         "finds": ["underside", "lintel", "sherd", "plate", "rim", "slab"]},
        "wall": load_yaml("wall.yaml"),
        "findings": load_yaml("findings.yaml")["findings"],
        "chronology": load_yaml("chronology.yaml")["events"],
        "claims": claims(figs),
        "metrics": metrics_subset(),
    }
    needles = sealed_needles()
    data["meta"]["leak"] = {"needles": len(needles), "hits": 0}
    leaks = export.leak_check(data, needles)
    if leaks:
        raise SystemExit("LEAK CHECK FAILED — the page was not written:\n  " + "\n  ".join(leaks[:20]))

    engine = (RR / "engine.js").read_text(encoding="utf-8")
    app = "\n".join(p.read_text(encoding="utf-8") for p in sorted((RR / "app").glob("*.js")))
    app = '(function () {\n"use strict";\n' + app + "\n})();"
    shell = (RR / "shell.html").read_text(encoding="utf-8")
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    page = (shell.replace("/*__DATA__*/", blob, 1)
                 .replace("/*__ENGINE__*/", engine.replace("</script", "<\\/script"), 1)
                 .replace("/*__APP__*/", app.replace("</script", "<\\/script"), 1))
    # the finished page gets the same check as its data
    for needle, what in needles.items():
        if needle in page:
            raise SystemExit(f"LEAK CHECK FAILED in the page text: {what}")
    (RR / "index.html").write_text(page, encoding="utf-8")
    print(f"reading_room/index.html: {len(page) / 1024:.0f} KB; {len(cat)} entries; "
          f"{len(needles)} sealed strings checked, none present")


if __name__ == "__main__":
    main()
