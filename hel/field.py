"""Field English: validation, inflection, and the naming generator.

Authority C. The register itself lives in ``data/field_english.yaml``; this module
keeps it honest (every loan points at a real unit; no apostrophes anywhere) and
implements Phase 2 plan item 1 — **generative naming rules, not a list** (benchmark
C13 scores a fixed list 3/5).
"""
from __future__ import annotations

import random
import re
from pathlib import Path

import yaml

from . import grammar as g

PATH = Path(__file__).resolve().parent.parent / "data" / "field_english.yaml"


def load() -> dict:
    return yaml.safe_load(PATH.read_text(encoding="utf-8"))


def validate(data: dict | None = None, register_forms: set | None = None) -> list[str]:
    data = data or load()
    problems = []
    text = PATH.read_text(encoding="utf-8")
    known = {f.form for f in g.FORMATIVES} | (register_forms or set())
    # the ASCII rule governs substrate-derived spellings, not English prose: no loan is
    # ever written with an apostrophe, bare or inflected (kalsiraed, never kalsira'd)
    for e in data["loans"]:
        if "'" in e["loan"]:
            problems.append(f"{e['loan']}: apostrophe in a loan")
    for unit in sorted(known, key=len, reverse=True):
        if len(unit) >= 3 and re.search(rf"\b{re.escape(unit)}'[a-z]", text):
            problems.append(f"{unit}: written with an apostrophe inflection")
    for e in data["loans"]:
        unit = str(e.get("source", {}).get("unit", ""))
        head = unit.split()[0] if unit else ""
        if head and not head.startswith(("CSC-", "[", "the", "hilun-to")) and head not in known:
            problems.append(f"{e['loan']}: source unit {head!r} is not a registered unit or formative")
    return problems


def inflect(loan: str, form: str) -> str:
    """English inflection of a loan, ASCII-clean. Vowel-final stems take -ed and -s
    without elision (the style manual forbids apostrophes, so kalsira'd is written
    kalsiraed); consonant-final stems double a final single consonant after a short
    stressed vowel in the Field pronunciation (tul > tulled)."""
    if form == "plural":
        return loan + ("es" if loan.endswith("s") else "s")
    if form == "past":
        if loan[-1] in "aeiou":
            return loan + "ed"
        if len(loan) <= 4 and re.search(r"[aeiou][^aeiouwy]$", loan):
            return loan + loan[-1] + "ed"
        return loan + "ed"
    if form == "gerund":
        if len(loan) <= 4 and re.search(r"[aeiou][^aeiouwy]$", loan):
            return loan + loan[-1] + "ing"
        return loan + "ing"
    raise ValueError(form)


# --- the naming generator ---------------------------------------------------------

SHAPES = ["Ladder", "Comb", "Hook", "Fork", "Stair", "Needle", "Hinge", "Knot", "Spur", "Keel"]
INTERVALS = ["Long Wait", "Short Hour", "Second Dawn", "Slow Door", "Dry Month", "Late Tide"]
QUIET = ["Quiet", "Slow", "Cold", "Blind", "Still", "Low"]
NUMBERS = ["Four", "Nine", "Twelve", "Sixteen", "Twenty", "Thirty-One"]


def name(kind: str, rng: random.Random, **ctx) -> dict:
    """Coin a field name by one of the stated rules. Returns the name and its rule —
    the rule is what makes a name *unrenameable* once routes are catalogued under it.

    kind:
      shape    — from a deprecated reading of a trace's shape (the Ladder)
      find     — from a find circumstance (the 1897 underside)
      interval — from an interval at a locus (the Long Wait)
      failure  — from a failure, cover-term style (Quiet Sixteen)
    """
    if kind == "shape":
        n = f"the {rng.choice(SHAPES)}"
        why = "named for a reading of the trace's shape that has since been deprecated; kept because the routes are catalogued under it"
    elif kind == "find":
        n = f"the {ctx.get('year', 1900)} {rng.choice(['underside', 'lintel', 'sherd', 'plate', 'rim', 'slab'])}"
        why = "named for the circumstance of its finding, as the style manual prefers for anything without a reading"
    elif kind == "interval":
        n = f"the {rng.choice(INTERVALS)}"
        why = "named for an interval a crew spent there; outlives the crew and the interval"
    elif kind == "failure":
        n = f"{rng.choice(QUIET)} {rng.choice(NUMBERS)}"
        why = "a cover term: deliberately mundane, assigned after a failure so that the failure has a name that says nothing"
    else:
        raise ValueError(kind)
    return {"name": n, "rule": kind, "why": why}
