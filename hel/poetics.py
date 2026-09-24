"""P-III: the poetics Stratum III is composed under.

Authority C. PRODUCTION (sealed key P-III): these are compositional rules, and the
sealed register records the rule each text was built under — never a meaning,
because there is none to record (A-reserve §6.6). Random syllables satisfying the
classifier would be worthless (A-reserve §6.3 rule 4); every text here has a form,
a scheme, and a vocabulary chosen for it.

Forms (each yields length ≡ 0 mod 3 unless it is a declared exception):

* **triad** — three-unit groups; a refrain closes every group; the first group's
  opening returns at the head of the last (the envelope). CSC-1146 is a triad.
* **anaphora** — every group opens on the same unit.
* **chain** — each group opens on the unit that closed the one before (anadiplosis).
* **ring** — the second half returns the first half's units in reverse.
* **litany** — a refrain every group, and a fixed pair inside every group.

A terminal-syllable scheme is laid over every form: the groups' final syllables
repeat or transpose (groups 1 and 3 identical, group 2 a transposition, in CSC-1146).
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field

from . import coin
from . import phonology as ph

CSC_1146 = ("walnisen pehisar tirakur pekalar munlisen tirakur walnisen nusar tirakur").split()


@dataclass
class Text:
    units: list[str]
    form: str
    rule: dict = field(default_factory=dict)        # the sealed register entry


def _vocab(n: int, rng: random.Random, exclude: set, lexicon, shared_pool: list, share_p: float):
    words = coin.coin_iii(n, rng, exclude, lexicon)
    # alliteration: a text's units tend to share an opening syllable (A-reserve §4.6)
    if len(words) >= 3 and rng.random() < 0.6:
        head = ph.syllables(words[0])[0]
        for i in range(1, len(words)):
            if rng.random() < 0.35:
                cand = head + "".join(ph.syllables(words[i])[1:])
                # a respelled unit is a new coinage and passes the same screen
                if (ph.is_transliteration(cand) and cand not in exclude and cand not in words
                        and coin.sc.passes(cand)):
                    words[i] = cand
    if shared_pool and rng.random() < share_p:
        words[-1] = rng.choice(shared_pool)
    return words


def compose(form: str, groups: int, rng: random.Random, exclude: set, lexicon,
            shared_pool=(), share_p: float = 0.12) -> Text:
    n_types = {"triad": 2 + groups, "anaphora": 2 + groups, "chain": 2 + groups,
               "ring": max(3, groups + 1), "litany": 3 + groups}[form]
    n_types = max(3, min(n_types, 3 * groups - 1))
    V = _vocab(n_types, rng, exclude, lexicon, list(shared_pool), share_p)
    units = []
    if form == "triad":
        refrain, envelope = V[0], V[1]
        others = V[2:] or [V[1]]
        for gi in range(groups):
            a = envelope if gi in (0, groups - 1) else others[gi % len(others)]
            b = others[(gi + 1) % len(others)]
            units += [a, b, refrain]
    elif form == "anaphora":
        opener = V[0]
        rest = V[1:]
        for gi in range(groups):
            units += [opener, rest[(2 * gi) % len(rest)], rest[(2 * gi + 1) % len(rest)]]
    elif form == "chain":
        prev = V[0]
        k = 1
        for gi in range(groups):
            nxt = V[k % len(V)]; mid = V[(k + 1) % len(V)]
            units += [prev, mid, nxt]
            prev, k = nxt, k + 2
    elif form == "ring":
        n = 3 * groups
        half = [V[i % len(V)] for i in range(n // 2)]
        pivot = [V[len(half) % len(V)]] if n % 2 else []
        units = half + pivot + half[::-1]
    elif form == "litany":
        refrain, p1, p2 = V[0], V[1], V[2]
        rest = V[3:] or [V[1]]
        for gi in range(groups):
            units += [p1 if gi % 2 == 0 else p2, rest[gi % len(rest)], refrain]
    rule = {"form": form, "groups": groups, "types": len(set(units)),
            "refrain": units[2] if form in ("triad", "litany") else None,
            "terminal_scheme": [ph.syllables(u)[-1] for u in units]}
    return Text(units, form, rule)


def csc_1146() -> Text:
    return Text(list(CSC_1146), "triad", {
        "form": "triad", "groups": 3, "types": 6, "refrain": "tirakur", "envelope": "walnisen",
        "terminal_scheme": ["sen", "sar", "kur", "lar", "sen", "kur", "sen", "sar", "kur"],
        "placement": "the underside of a portable object; no face bears a trace line",
        "affect": "recognition by the third return; the short penultimate unit is where the line catches",
        "withheld": "nothing is withheld because no meaning was fixed by anyone, including the author",
        "hand_composed": True,
    })


def exception(kind: str, rng: random.Random, exclude: set, lexicon) -> Text:
    """The declared exceptions to length ≡ 0 mod 3 (A-reserve §4.1)."""
    if kind == "contested-7":
        from .parse import assignable
        for _ in range(400):
            t = compose("triad", 2, rng, exclude, lexicon)
            # one unit whose boundary is contested: the Standard counts it as two. Both
            # halves must themselves be unassignable, or the text would fail Condition 1
            # and could not be Stratum III at all (the first Phase 2 build filed three
            # texts whose split left a bare warrant, grade or scope unit — nes, lan, kur —
            # and forced them into the class; the classifier had rejected them)
            s = ph.syllables(t.units[1])
            if len(s) < 3:
                continue
            a, b = "".join(s[:2]), "".join(s[2:])
            if any(assignable(x, lexicon) or x in exclude or not coin.sc.passes(x) for x in (a, b)):
                continue
            t.units[1:2] = [a, b]
            t.rule["exception"] = "seven units under the Standard; six under the contested boundary"
            t.form = "triad (contested)"
            return t
        raise RuntimeError("no contested-boundary text could be composed")
    t = compose("anaphora", 3, rng, exclude, lexicon)
    cut = rng.choice((8, 10))
    t.units = t.units[:cut] if cut < len(t.units) else t.units + [t.units[0]]
    t.rule["exception"] = "Ch-2 plate: the field's extent is a judgement call"
    t.form = "anaphora (extent judged)"
    return t
