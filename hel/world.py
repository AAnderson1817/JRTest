"""SEALED. The network the corpus is rendered from.

Reads ``sealed/key.yaml``. Authority C. Author-side only: nothing in this module is
published, and ``hel.export`` refuses to ship anything it produces.

The world is a directed network of loci joined by one-way links (canon A: streams are
fixed, one-directional, interlocking loops). It is observed in *epochs* — discrete
passes of the network, five calendar years each across HEL's cataloguing era — and a
coordinate's condition (the thing a root correlates with, per the sealed key) is
computed from the links' states in an epoch.

What is deliberately **not** here: anything about who or what built the network, what
records are for, or why records correlate with it. The builders are not represented,
not even as an absence.
"""
from __future__ import annotations

import random
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml

ROOT = Path(__file__).resolve().parent.parent
KEY_PATH = ROOT / "sealed" / "key.yaml"

N_LOCI = 360
EPOCHS = 31                  # 1874–2028 in five-year passes; epoch of a year: (y-1874)//5
FIRST_YEAR = 1874


def epoch_of(year: int) -> int:
    return max(0, min(EPOCHS - 1, (year - FIRST_YEAR) // 5))


def load_key() -> dict:
    return yaml.safe_load(KEY_PATH.read_text(encoding="utf-8"))


@dataclass
class Link:
    lid: int
    src: int
    dst: int                    # nominal destination
    kind: str                   # direct | forced | displacing | returning
    actual: int                 # where it actually lands (== dst unless displacing)
    sign: int                   # +1 emerges ahead, -1 behind, 0 level
    magnitude: float            # days, typical |displacement| (HEL's logs have it)
    status: list = field(default_factory=list)     # per epoch: open | closed | dormant
    closed_every: bool = False
    period: int = 0             # >0: available one epoch in `period`
    traversals: list = field(default_factory=list)  # per epoch: count
    sign_varies: bool = False   # the displacement's sign differs between passes (key: nikur)

    def open_in(self, e: int) -> bool:
        return self.status[e] == "open"


@dataclass
class Locus:
    idx: int
    dwell: bool = False          # arrivals dwell before any departure (key: held)
    standing: bool = False       # Ch-2 standing patterns form here
    modulating: bool = False     # Ch-3 recordable in traversals from here
    find_rich: float = 1.0       # relative abundance of recoverable objects
    bind_partner: bool = False   # carries a second description

    @property
    def name(self) -> str:
        return f"L-{self.idx}"


class World:
    """The network, built deterministically from a seed."""

    def __init__(self, seed: int = 1908):
        self.rng = random.Random(seed)
        self.key = load_key()
        self.loci = [Locus(i) for i in range(N_LOCI)]
        self.links: list[Link] = []
        self.out = defaultdict(list)
        self.inn = defaultdict(list)
        self.cycles: list[list[int]] = []
        self.forced_through: set[int] = set()
        self.pins: dict[str, int] = {}
        self._build()

    # -------------------------------------------------------------- construction
    def _add(self, src, dst, kind, actual=None, sign=None):
        rng = self.rng
        if sign is None:
            sign = rng.choices((1, -1, 0), (0.46, 0.18, 0.36))[0]
        mag = 0.0 if sign == 0 else round(rng.lognormvariate(4.2, 1.1), 1)
        link = Link(len(self.links), src, dst, kind, dst if actual is None else actual, sign, mag)
        self.links.append(link)
        self.out[src].append(link)
        self.inn[link.actual].append(link)
        return link

    def _build(self):
        rng = self.rng
        n = N_LOCI
        pool = list(range(1, n))
        # 1. interlocking loops: cycles over overlapping subsets
        for _ in range(70):
            k = rng.choice((3, 3, 4, 4, 5, 5, 6, 7, 8, 9, 11))
            cyc = rng.sample(pool, k)
            self.cycles.append(cyc)
            for a, b in zip(cyc, cyc[1:] + cyc[:1]):
                if not any(l.dst == b for l in self.out[a]):
                    self._add(a, b, "direct")
        # 2. nested loops: a short cycle through two nodes of a long one
        for cyc in [c for c in self.cycles if len(c) >= 6][:12]:
            a, b = cyc[0], cyc[len(cyc) // 2]
            mid = rng.choice(pool)
            self._add(a, mid, "direct"); self._add(mid, b, "direct")
            self.cycles.append([a, mid, b] + cyc[len(cyc) // 2 + 1:])
        # 3. chords between loops
        for _ in range(150):
            a, b = rng.sample(pool, 2)
            if not any(l.dst == b for l in self.out[a]):
                self._add(a, b, "direct")
        # 4. forced legs: a link into a through-node (entered only to be left)
        cand = [v for v in pool if len(self.out[v]) >= 1 and len(self.inn[v]) >= 1]
        for v in rng.sample(cand, 38):
            for l in self.inn[v][:1]:
                l.kind = "forced"
            self.forced_through.add(v)
        # 5. displacing links: land at a neighbour of the nominal destination
        for l in rng.sample([l for l in self.links if l.kind == "direct"], 70):
            nbrs = [m.dst for m in self.out[l.dst] if m.dst != l.src] or [rng.choice(pool)]
            actual = rng.choice(nbrs)
            self.inn[l.actual].remove(l)
            l.kind, l.actual = "displacing", actual
            self.inn[actual].append(l)
        # 6. returning links: back to a similar, non-identical coordinate on the same loop
        for cyc in rng.sample(self.cycles, 34):
            a = rng.choice(cyc)
            self._add(a, a if rng.random() < 0.5 else rng.choice(cyc), "returning", sign=rng.choice((1, -1)))
        # 7. sinks and sources
        sinks = rng.sample(pool, 22)
        for s in sinks:
            for l in list(self.out[s]):
                self.inn[l.actual].remove(l)
                self.links.remove(l)
            self.out[s] = []
        self.links = [l for l in self.links]
        for i, l in enumerate(self.links):
            l.lid = i
        # 8. static locus properties
        for loc in self.loci[1:]:
            loc.dwell = rng.random() < 0.11
            loc.standing = rng.random() < 0.16
            loc.modulating = rng.random() < 0.13
            loc.find_rich = rng.lognormvariate(0, 0.7)
            loc.bind_partner = rng.random() < 0.07
        # 9. HEL's departure locus: L-0. Linked in and out so expeditions can leave and
        #    (sometimes) come home. Nothing is ever recovered at L-0 (withheld, #15).
        for b in rng.sample(pool, 9):
            self._add(0, b, "direct", sign=0)
        for a in rng.sample(pool, 12):
            self._add(a, 0, "direct", sign=0)
        # 10. monotone sign along forced paths (sealed: Sturge undecidable by construction)
        for v in self.forced_through:
            into = [l for l in self.inn[v] if l.kind == "forced"]
            if into:
                for l in self.out[v]:
                    l.sign = into[0].sign if into[0].sign != 0 else l.sign
        self._statuses()
        self._pin()

    def _statuses(self):
        rng = self.rng
        for l in self.links:
            l.sign_varies = rng.random() < 0.08
            base_closed = rng.random() < 0.10
            l.closed_every = base_closed and rng.random() < 0.35
            l.period = rng.choice((0, 0, 0, 0, 0, 2, 3, 4, 7)) if not l.closed_every else 0
            phase = rng.randrange(max(1, l.period))
            volatile = rng.random() < 0.18
            st = []
            for e in range(EPOCHS):
                if l.closed_every:
                    s = "closed"
                elif l.period and (e + phase) % l.period != 0:
                    s = "dormant"
                elif base_closed and rng.random() < 0.5:
                    s = "closed"
                elif volatile and rng.random() < 0.25:
                    s = rng.choice(("closed", "dormant"))
                else:
                    s = "open"
                st.append(s)
            l.status = st
            l.traversals = [(rng.randrange(0, 6) if s == "open" else 0) for s in st]

    # ------------------------------------------------------------------ pinned
    def _pin(self):
        """Loci the published record already names. Their conditions are set so that
        the documented incidents follow from the network rather than from narration."""
        rng = self.rng
        # L-31, the Long Wait: a dwell locus with one slow outbound route (A-reserve §8.3)
        l31 = self.loci[31]
        l31.dwell = True
        l31.find_rich = 3.0
        if not self.out[31]:
            self._add(31, rng.choice(range(40, 80)), "direct")
        for l in self.out[31]:
            l.period = 5
            l.status = ["open" if e % 5 == 2 else "dormant" for e in range(EPOCHS)]
        # L-9: HEL's map shows no outbound edge. It has one: displacing and long-period.
        for l in list(self.out[9]):
            self.inn[l.actual].remove(l); self.links.remove(l)
        self.out[9] = []
        leave = self._add(9, 120, "displacing", actual=rng.choice(range(200, 240)), sign=1)
        leave.period = 7
        leave.status = ["open" if e % 7 == 3 else "dormant" for e in range(EPOCHS)]
        self.loci[9].find_rich = 2.5
        # the Ladder: a standing junction H and a quiet K; K→H direct and always open
        H, K = 7, 104
        for l in list(self.out[K]):
            if l.dst == H:
                self.out[K].remove(l); self.inn[l.actual].remove(l); self.links.remove(l)
        for l in list(self.inn[K])[1:]:                   # K is quiet: one arrival at most
            self.out[l.src].remove(l); self.inn[K].remove(l); self.links.remove(l)
        ladder = self._add(K, H, "direct", sign=0)
        ladder.status = ["open"] * EPOCHS
        ladder.traversals = [0] * EPOCHS    # nobody has made the approach since 1948
        for _ in range(3 - len(self.out[H])):
            self._add(H, rng.choice(range(130, 170)), "direct")
        for l in self.out[H]:
            l.status = ["open"] * EPOCHS
        self.pins.update({"long_wait": 31, "sowerby": 9, "ladder_H": H, "ladder_K": K})
        # the Quiet Sixteen node: held, no direct departure, one displacing departure
        Q = 16
        self.loci[Q].dwell = True
        for l in list(self.out[Q]):
            self.inn[l.actual].remove(l); self.links.remove(l)
        self.out[Q] = []
        q = self._add(Q, 250, "displacing", actual=rng.choice(range(251, 290)), sign=1)
        q.magnitude = 427.0            # fourteen months, in HEL's log
        q.status = ["open"] * EPOCHS
        self.pins["quiet_sixteen"] = Q
        for i, l in enumerate(self.links):
            l.lid = i
            if len(l.status) != EPOCHS:
                l.status = ["open"] * EPOCHS
            if len(l.traversals) != EPOCHS:
                l.traversals = [(rng.randrange(0, 6) if s == "open" else 0) for s in l.status]

    # --------------------------------------------------------------- conditions
    def departures(self, v, e=None, kinds=None):
        ls = self.out[v]
        if kinds:
            ls = [l for l in ls if l.kind in kinds]
        if e is not None:
            ls = [l for l in ls if l.open_in(e)]
        return ls

    def arrivals(self, v, e=None):
        ls = self.inn[v]
        if e is not None:
            ls = [l for l in ls if l.open_in(e)]
        return ls

    def features(self, v: int, e: int) -> set[str]:
        """The sealed condition of coordinate (v, e): the set of root features true of it."""
        loc = self.loci[v]
        f = set()
        out_all, in_all = self.out[v], self.inn[v]
        out_open = [l for l in out_all if l.open_in(e)]
        prev = e - 1 if e > 0 else None
        tr = sum(l.traversals[e] for l in out_all + in_all)
        if len(out_open) >= 2:
            stable_frac = sum(len([l for l in out_all if l.open_in(x)]) >= 2 for x in range(EPOCHS)) / EPOCHS
            if stable_frac >= 0.8:
                f.add("standing_junction")
        if loc.dwell:
            f.add("held")
        if v in self.forced_through:
            f.add("through")
        if loc.standing:
            f.add("standing")
        if out_all and all(l.period for l in out_all):
            f.add("periodic")
        if len(in_all) <= 1:
            f.add("quiet")
        if not out_all:
            f.add("sink")
        if len({l.src for l in in_all}) >= 2:
            f.add("convergent")
        if out_all and all(l.status[e] == "dormant" for l in out_all):
            f.add("dormant")
        if any(l.status[e] == "closed" for l in out_all):
            f.add("closed_departure")
        if any(l.kind == "returning" for l in out_all):
            f.add("on_recur")
        if any(l.kind == "displacing" for l in in_all):
            f.add("displaced_arrival")
        signs = [l.sign for l in in_all]
        if signs and sum(s > 0 for s in signs) > len(signs) / 2:
            f.add("arrive_ahead")
        if signs and sum(s < 0 for s in signs) > len(signs) / 2:
            f.add("arrive_behind")
        if signs and all(s == 0 for s in signs):
            f.add("level")
        if tr >= 9:
            f.add("busy")
        if not in_all:
            f.add("source")
        if any(len(set(l.status)) > 1 and not l.period for l in out_all + in_all):
            f.add("volatile")
        if self._nested(v):
            f.add("nested")
        if len(in_all) == 1:
            f.add("singular")
        if loc.modulating:
            f.add("modulating")
        osigns = {l.sign for l in out_all}
        if len(osigns) >= 2:
            f.add("phase_split")
        if all(len(set(l.status)) == 1 for l in out_all + in_all) and (out_all or in_all):
            f.add("stable")
        if loc.bind_partner:
            f.add("bound")
        if len(out_all) + len(in_all) == 1:
            f.add("peripheral")
        if self._depth_from_junction(v) >= 4:
            f.add("deep")
        if in_all and all(l.status[e] == "closed" for l in in_all):
            f.add("closed_arrival")
        if len(out_all) == 2:
            f.add("two_departures")
        if self._cycle_entry(v):
            f.add("cycle_entry")
        if len(in_all) == 1 and len(out_all) == 1 and not loc.dwell and v not in self.forced_through:
            f.add("transit")
        if prev is not None and any(l.status[prev] == "dormant" and l.status[e] == "open" for l in out_all):
            f.add("waking")
        if len(in_all) >= 2 and len(out_all) >= 2:
            f.add("shared")
        if len({l.actual for l in out_all}) >= 2 and any(l.kind == "displacing" for l in out_all):
            f.add("scattering")
        if len({l.kind for l in out_all}) >= 2:
            f.add("mixed_kinds")
        if (out_all or in_all) and sum(l.traversals[e] for l in out_all + in_all) == 0:
            f.add("still")
        if len(in_all) >= 4:
            f.add("gathering")
        if out_all and not self._returns(v):
            f.add("no_return")
        if any(l.src in self.forced_through for l in in_all):
            f.add("forced_end")
        if loc.standing and loc.modulating:
            f.add("patterned")
        if any(l.closed_every for l in out_all):
            f.add("closed_every")
        if len(in_all) == 1 and len(out_all) == 1:
            f.add("corridor")
        if out_all and sum(l.sign < 0 for l in out_all) > len(out_all) / 2:
            f.add("departs_behind")
        if any(len(c) >= 8 and v in c for c in self.cycles):
            f.add("long_cycle")
        return f

    def _nested(self, v):
        mine = [c for c in self.cycles if v in c]
        return any(set(a) < set(b) or (len(set(a) & set(b)) >= 2 and len(a) < len(b))
                   for a in mine for b in self.cycles if a is not b)

    def _cycle_entry(self, v):
        mine = [set(c) for c in self.cycles if v in c]
        return bool(mine) and any(l.src not in c for l in self.inn[v] for c in mine)

    def _depth_from_junction(self, v, cap=6):
        """Links back (against direction) to the nearest node with 2+ departures."""
        frontier, seen = {v}, {v}
        for d in range(cap):
            if any(len(self.out[u]) >= 2 for u in frontier if u != v):
                return d
            nxt = {l.src for u in frontier for l in self.inn[u]} - seen
            if not nxt:
                return cap
            seen |= nxt
            frontier = nxt
        return cap

    def _returns(self, v, depth=3):
        origins = {l.src for l in self.inn[v]}
        frontier, seen = {v}, {v}
        for _ in range(depth):
            nxt = {l.actual for u in frontier for l in self.out[u]} - seen
            if nxt & origins:
                return True
            seen |= nxt
            frontier = nxt
        return False
