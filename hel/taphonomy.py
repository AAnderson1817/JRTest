"""Damage and attrition (benchmark Design rule 3, second half; Phase 1 import H4).

Authority C. Damage is applied to rendered records and never authored. Every loss is
logged on the record, so a catalogued fragment can always be traced back to its
intact form (C4: "every fragment derived from it with a rule trace on demand").

The model, stated as rules with rates, so C4's audit is mechanical (Phase 1 §4.4, H4):

* **Condition** of a Ch-1 object: intact / worn / fractured / eroded, drawn per object.
* **Warrant ticks go first.** They sit off the line on lead-lines (A §9); a lost tick
  leaves a segment catalogued *damaged*, not *unwarranted*.
* **Cartouche interiors are the shallowest incision** (A §9): a worn cartouche loses
  slots — lost, which is not the same as ``hilun`` (ruled empty).
* **Margins break.** A fracture takes the end of a chain; the surviving half becomes
  ``-ken ⌀``. This, and nothing else, is where broken halves come from.
* **Intervals erode.** An eroded interval leaves a line with a flick nobody can read;
  both halves become illegible (transcribed ADJ by the Standard — see ``hel.archive``).
* **H4, human transmission:** head halves are spoken unstressed and fast, so oral
  transmission eats them — the Ch-4 formulae are full of tails without heads.
"""
from __future__ import annotations

import copy
import random

from . import grammar as g

CONDITION_RATES = {"intact": 0.36, "worn": 0.22, "fractured": 0.32, "eroded": 0.10}
LOSE_WARRANT = {"intact": 0.0, "worn": 0.22, "fractured": 0.40, "eroded": 0.65}
LOSE_SLOT = {"intact": 0.0, "worn": 0.12, "fractured": 0.18, "eroded": 0.45}
FRACTURE_END = {"intact": 0.0, "worn": 0.18, "fractured": 0.88, "eroded": 0.62}
ERODE_INTERVAL = {"intact": 0.0, "worn": 0.16, "fractured": 0.18, "eroded": 0.45}
H4_HEAD_LOSS = 0.45     # per head half, per generation of oral transmission


def draw_condition(rng: random.Random) -> str:
    return rng.choices(list(CONDITION_RATES), list(CONDITION_RATES.values()))[0]


def damage(rec, condition: str, rng: random.Random, last_on_object: bool = True):
    """Return a damaged deep copy of ``rec`` with ``rec.damage`` logged."""
    r = copy.deepcopy(rec)
    r.condition = condition
    log = []
    seg = r.seg
    if condition == "intact":
        r.damage = log
        return r
    # margins: a fracture takes the end of the chain (the object's edge)
    if last_on_object and len(seg.words) >= 2 and rng.random() < FRACTURE_END[condition]:
        lost = 1 if len(seg.words) == 2 or rng.random() < 0.8 else 2
        if lost >= len(seg.words):
            lost = len(seg.words) - 1
        # production constraint, not taphonomy: a fracture never strands a -mun tail, so
        # the catalogue's half-negation count stays the one A §4.4 states (23)
        strands_mun = seg.words[-lost - 1].polarity == "mun" and seg.words[-lost - 1].tail
        if rng.random() < 0.72 and not strands_mun:
            gone = seg.words[-lost:]
            seg.words = seg.words[:-lost]
            log.append(("margin-end", [w.root for w in gone]))
        else:
            gone = seg.words[:lost]
            seg.words = seg.words[lost:]
            log.append(("margin-start", [w.root for w in gone]))
        seg.warrants = [] if rng.random() < 0.85 else seg.warrants
        if not seg.warrants:
            log.append(("warrant", "lost with the margin"))
    # warrant ticks on their lead-lines
    if seg.warrants and rng.random() < LOSE_WARRANT[condition]:
        log.append(("warrant", list(seg.warrants)))
        seg.warrants = []
    # cartouche interiors
    for w in seg.words:
        if w.coord is not None:
            slots = list(w.coord.slots())
            for i in range(3):
                if slots[i] is not None and rng.random() < LOSE_SLOT[condition]:
                    log.append(("slot", ("LOCUS", "PASS", "PHASE")[i]))
                    slots[i] = None
            w.coord = g.Coordinate(*slots)
    # eroded intervals: the flick survives as a mark nobody can class
    for i in range(len(seg.words) - 1):
        a, b = seg.words[i], seg.words[i + 1]
        if a.tail and b.head and a.tail == b.head and rng.random() < ERODE_INTERVAL[condition]:
            log.append(("interval", a.tail))
            a.tail_illegible = True
            b.head_illegible = True
    r.damage = log
    return r


def oral(rec, generations: int, rng: random.Random):
    """H4: what recitation eats. Returns a copy with head halves dropped at the stated
    rate per generation, and the loss logged."""
    r = copy.deepcopy(rec)
    log = []
    for w in r.seg.words:
        if w.head:
            p_keep = (1 - H4_HEAD_LOSS) ** generations
            if rng.random() > p_keep:
                log.append(("h4-head", w.head))
                w.head = None
    r.damage = getattr(r, "damage", []) + log
    return r
