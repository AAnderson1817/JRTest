"""Coining forms under the 1908 code's constraints, screened.

Authority C. Used for the non-core functional roots (the no-gloss zone and the long
tail of the register) and for Stratum III vocabulary. Every coined form is checked
against the sanctioned list, the shape rules, the register, and the collision screen
(``hel.screen``); rejects are kept, because a rejects list is the only evidence a
screen was run (A §6.1f).
"""
from __future__ import annotations

import random

from . import phonology as ph
from . import screen as sc

OPEN, CLOSED, ONSET0 = ph.OPEN, ph.CLOSED, ph.ONSETLESS


def _shape_root(rng: random.Random) -> list[str]:
    """Shapes of functional roots: vowel-final, 2-4 syllables, coda if 3+."""
    shape = rng.choices(
        ["CV.CV", "CVC.CV", "CVC.CV.CV", "CV.CVC.CV", "CVC.CVC.CV", "V.CV.CV", "CV.CV.CVC.CV", "CVC.CV.CV.CV"],
        [10, 14, 34, 18, 7, 40, 6, 6])[0]
    out = []
    for i, part in enumerate(shape.split(".")):
        if part == "V":
            out.append(rng.choice(ONSET0))
        elif part == "CVC":
            out.append(rng.choice(CLOSED))
        else:
            out.append(rng.choice(OPEN))
    return out


def _shape_iii(rng: random.Random) -> list[str]:
    """Stratum III silhouette (A-reserve §4.6): longer, coda-final, onsets repeat."""
    n = rng.choices([2, 3, 4], [22, 50, 28])[0]
    out = [rng.choice(OPEN + CLOSED) for _ in range(n - 1)]
    out.append(rng.choice(CLOSED) if rng.random() < 0.86 else rng.choice(OPEN))   # mostly coda-final
    return out


def _ok_sequence(sylls: list[str]) -> bool:
    for a, b in zip(sylls, sylls[1:]):
        if ph.coda(a) and ph.onset(b) == ph.coda(a):
            return False           # geminate
        if b in ONSET0:
            return False           # onsetless only initially
    return True


def coin_roots(n: int, rng: random.Random, exclude: set[str], screen: bool = True,
               rejects: dict | None = None) -> list[str]:
    from .grammar import FORMATIVES
    bound = {f.form for f in FORMATIVES}
    out, tries = [], 0
    while len(out) < n and tries < n * 400:
        tries += 1
        s = _shape_root(rng)
        if not _ok_sequence(s):
            continue
        form = "".join(s)
        if form in exclude or form in bound or form in out:
            continue
        ok, _ = ph.licensed_as_root(form)
        if not ok:
            continue
        if ph.segment(form) and len(ph.segment(form)) > 1:
            continue                 # keep the functional register unambiguous
        if screen and not sc.passes(form):
            if rejects is not None:
                rejects[form] = [(h.entry.text, h.entry.category, h.entry.family) for h in sc.screen(form)[:2]]
            continue
        out.append(form)
    return out


def coin_iii(n: int, rng: random.Random, exclude: set[str], lexicon, screen: bool = True,
             rejects: dict | None = None) -> list[str]:
    from .parse import assignable
    out, tries = [], 0
    while len(out) < n and tries < n * 500:
        tries += 1
        s = _shape_iii(rng)
        if not _ok_sequence(s):
            continue
        form = "".join(s)
        if form in exclude or form in out:
            continue
        if assignable(form, lexicon):
            continue
        if screen and not sc.passes(form):
            if rejects is not None:
                rejects[form] = [(h.entry.text, h.entry.category, h.entry.family) for h in sc.screen(form)[:2]]
            continue
        out.append(form)
    return out
