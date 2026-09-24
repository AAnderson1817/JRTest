"""The unit register: the published face of the ~90-unit analyzable core and the
wider catalogue of recurring roots.

Authority C. Reads ``data/lexicon.json`` — published fields only. Nothing in this
module reads ``sealed/``; the sealed correlates of the core live in
``hel.sealed`` and are joined only by modules that say so.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from . import phonology as ph

ROOT = Path(__file__).resolve().parent.parent
LEXICON_PATH = ROOT / "data" / "lexicon.json"


@dataclass
class Unit:
    cid: str                 # "CSC-0012"
    form: str                # 1988 Reformed List transliteration
    kind: str                # "root" | "ritual"
    gloss: Optional[str]     # the Archive's queried gloss, or None (no-gloss zone)
    grade: str               # G0-G5, or "—" for no reading
    core: bool = False       # in the ~90-unit analyzable core
    commanded: bool = False  # may lawfully appear in a spoken route command (A §6.1d)
    channels: tuple = ()
    note: str = ""
    readings: list = field(default_factory=list)   # standing readings (school, gloss)

    @property
    def catalog_gloss(self) -> str:
        """Interlinear form, A §6.3: roots at G3 or worse in catalog form."""
        num = self.cid.replace("CSC-", "CSC.")
        if self.gloss is None:
            return f"{num}(?)"
        return f"{num}({self.gloss}?)"


class Lexicon:
    def __init__(self, units: list[Unit]):
        self.units = units
        self.by_form = {u.form: u for u in units}
        self.by_id = {u.cid: u for u in units}

    def root(self, form: str) -> Optional[Unit]:
        u = self.by_form.get(form)
        return u if u and u.kind == "root" else None

    def is_registered_root(self, form: str) -> bool:
        return self.root(form) is not None

    def is_ritual(self, form: str) -> bool:
        u = self.by_form.get(form)
        return bool(u and u.kind == "ritual")

    def core(self):
        return [u for u in self.units if u.core]

    def commanded(self):
        return [u for u in self.units if u.commanded]


def load(path: Path = LEXICON_PATH) -> Lexicon:
    data = json.loads(path.read_text(encoding="utf-8"))
    units = []
    for d in data["units"]:
        d = dict(d)
        d["channels"] = tuple(d.get("channels", ()))
        units.append(Unit(**d))
    return Lexicon(units)


_CACHE: Optional[Lexicon] = None


def default() -> Lexicon:
    global _CACHE
    if _CACHE is None:
        _CACHE = load()
    return _CACHE


def validate(lex: Lexicon) -> list[str]:
    """Structural checks every register revision must pass."""
    problems = []
    forms = [u.form for u in lex.units]
    if len(forms) != len(set(forms)):
        problems.append("duplicate forms in the register")
    for u in lex.units:
        if u.kind == "root":
            ok, why = ph.licensed_as_root(u.form)
            if not ok:
                problems.append(f"{u.cid} {u.form}: {why}")
        elif not ph.is_transliteration(u.form):
            problems.append(f"{u.cid} {u.form}: not built from the 1908 list")
    from .grammar import FORMATIVES
    bound = {f.form for f in FORMATIVES}
    for u in lex.units:
        if u.form in bound:
            problems.append(f"{u.cid} {u.form}: collides with a formative")
    commanded = [u.form for u in lex.commanded()]
    from .grammar import PASS_VALUES, PHASE_VALUES, WARRANTS, GAP
    free = [GAP] + list(PASS_VALUES) + list(PHASE_VALUES) + [w for w in WARRANTS if w != "[41]"]
    clash = ph.initial_distinctness(commanded + free)
    if clash:
        problems.append(f"commanded core shares first syllables: {clash}")
    if len(commanded) + len(free) > ph.commanded_core_cap():
        problems.append("commanded core exceeds the forty-eight-unit cap")
    return problems
