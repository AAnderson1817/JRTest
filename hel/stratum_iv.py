"""P-IV: Stratum IV, the Ch-3 modulation material.

Authority C. PRODUCTION (sealed key P-IV): a procedure with no truth value. It was
built so that a one-system story (IV is the same notation recorded through an
instrument) and a two-system story (IV is something else that shares thirty units
by coincidence or consolidation) fit its output equally well.

What it guarantees, because A §7 and §4.6a say so:

* **~30 units shared with Strata I–III**, and a larger IV-only inventory.
* **A sequencing constraint the other strata violate:** every log is a run of
  three-unit frames — frame mark, shared unit, IV-only value — and no unit recurs
  inside any window of four. Functional segments break that constantly (``ru ru``
  at every complete PASS edge).
* **Exactly two logs contain both ``tul`` and ``halu``** — the only two contrasts that
  would keep SHUNT and RECUR apart if Palimpsest is false (A §4.6a; Vance 2004).
"""
from __future__ import annotations

import random

from . import coin

SHARED = ("ru ken tul pel halu sil in is ar ol ti ka lan kas mun sen nir lus "
          "sa to nu kihar pukal rolun nikur hilun nes tir rukalti kasluhi").split()
KIND_BIAS = {"direct": "ru", "forced": "ken", "displacing": "tul", "returning": "halu"}


class IVGenerator:
    def __init__(self, rng: random.Random, lexicon, exclude: set):
        self.rng = rng
        pool = coin.coin_iii(42, rng, exclude, lexicon)
        self.frames = pool[:6]
        self.values = pool[6:]

    def log(self, link_kind: str, frames: int, contrast: bool = False) -> list[str]:
        rng = self.rng
        out: list[str] = []
        for f in range(frames):
            for _ in range(50):
                fm = rng.choice(self.frames)
                sh = KIND_BIAS[link_kind] if rng.random() < 0.3 else rng.choice(SHARED)
                if contrast and f == 0:
                    sh = "tul"
                if contrast and f == 1:
                    sh = "halu"
                if not contrast and link_kind != "returning" and sh == "halu":
                    continue
                if not contrast and link_kind == "returning" and sh == "tul":
                    continue
                vl = rng.choice(self.values)
                cand = out + [fm, sh, vl]
                if all(len(set(cand[i:i + 4])) == len(cand[i:i + 4]) for i in range(max(0, len(cand) - 6), len(cand))):
                    out = cand
                    break
        return out


def violates_iv_constraint(tokens: list[str]) -> bool:
    return any(len(set(tokens[i:i + 4])) < len(tokens[i:i + 4]) for i in range(len(tokens)))
