"""The only door out. Builds the published catalogue and checks it for leaks.

Authority C. Anything shipped — the Reading Room artifact, the decipherment-trial
packet, a Phase 3 corpus item — is built from ``published()`` and nothing else.
``leak_check`` fails if a sealed field, a root's sealed correlate, a damage log (which
would reveal an intact original), or a compositional rule survives into the output.
"""
from __future__ import annotations

import json
import re

from . import grammar as g

SEALED_KEYS = {"sealed", "truth", "damage", "iii_rule", "features", "loci", "links", "pin",
               "production", "verdict", "made_at", "epoch", "stratum_draw"}


def entry_public(e, lex) -> dict:
    d = {
        "ref": e.ref, "cid": e.cid, "part": e.part, "channel": e.channel, "stratum": e.stratum,
        "source": e.source, "locus": e.locus, "accession_year": e.accession_year,
        "catalogued_year": e.catalogued_year, "condition": e.condition,
        "field_name": e.field_name, "iii_position": e.iii_position, "notes": list(e.notes),
        "segments": [], "units": list(e.units),
    }
    for s in e.segments:
        findings = [(f.code, f.severity, f.where, f.message) for f in g.check(s, e.channel)
                    if f.severity != "note"]
        d["segments"].append({
            "translit": s.translit(),
            "gloss": g.gloss_lines(s, lex),
            "profile": g.stratum_profile(s),
            "findings": findings,
            "tokens": len(s.tokens()),
        })
    reg = e.register or {}
    if reg.get("env"):
        d["register"] = {"stratum_II_environments": [
            {k: v for k, v in x.items() if k in ("root", "trace", "older_branch_cut")} for x in reg["env"]]}
    if reg.get("copy"):
        d.setdefault("register", {})["copy_variants"] = reg["copy"]
    if reg.get("page_end_ar"):
        d.setdefault("register", {})["page_break_marked"] = True
    return d


def published(build) -> dict:
    lex = build.published_lexicon
    return {
        "catalogue": [entry_public(e, lex) for e in build.entries],
        "figures": build.figures,
        "iii_figures": build.iii_figures,
        "register": [{"cid": u.cid, "form": u.form, "kind": u.kind, "gloss": u.gloss, "grade": u.grade,
                      "core": u.core, "commanded": u.commanded, "note": u.note} for u in lex.units],
    }


def leak_check(obj, sealed_forms: dict | None = None) -> list[str]:
    """Walk the published object; report any sealed key or any sealed correlate text."""
    problems = []

    def walk(x, path="$"):
        if isinstance(x, dict):
            for k, v in x.items():
                if k in SEALED_KEYS:
                    problems.append(f"sealed key {k!r} at {path}")
                walk(v, f"{path}.{k}")
        elif isinstance(x, list):
            for i, v in enumerate(x):
                walk(v, f"{path}[{i}]")
    walk(obj)
    text = json.dumps(obj)
    for needle, what in (sealed_forms or {}).items():
        # a sealed definition, or a sealed compound-condition name, in shipped text is a leak.
        # (A published gloss that happens to match the truth is not: it is HEL's reading.)
        if needle and needle in text:
            problems.append(f"sealed text {needle!r} ({what}) appears in published text")
    return problems
