"""SEALED. Rendering records from the world (benchmark Design rule 3, first half).

Reads the world and the sealed key. Authority C. A *record* here is a segment exactly
as made — before damage, before any human copied it, before the 1908 committee cut
it. ``hel.taphonomy`` damages records; ``hel.archive`` transcribes and catalogues
them. Nothing downstream may edit a record's content except through those two stages.

Every record carries a ``truth`` dict (sealed): which loci and links it describes,
the epoch it was made in, which feature each root was chosen for, and the true scope
of any polarity. ``hel.export`` strips it.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Optional

from . import grammar as g
from . import phonology as ph
from .world import World, EPOCHS

KIND_CLASS = {"direct": "PASS", "forced": "THRU", "displacing": "SHUNT", "returning": "RECUR"}

#: PRODUCTION parameter (no truth value): how often a record-maker states each
#: condition when a coordinate is in several. Tuned only for corpus shape.
SALIENCE = {
    "standing_junction": 7, "held": 6, "through": 6, "standing": 4, "periodic": 3,
    "quiet": 4, "sink": 5, "convergent": 3, "dormant": 4, "closed_departure": 4,
    "on_recur": 4, "displaced_arrival": 4, "arrive_ahead": 3, "arrive_behind": 3,
    "busy": 4, "source": 2, "volatile": 2, "nested": 2, "singular": 2, "modulating": 3,
    "phase_split": 2, "stable": 3, "bound": 3, "deep": 2, "peripheral": 3,
    "closed_arrival": 4, "two_departures": 3, "cycle_entry": 2, "transit": 3,
    "level": 3, "waking": 3, "shared": 9, "scattering": 9, "mixed_kinds": 9,
    "still": 9, "gathering": 0.7, "no_return": 0.25, "forced_end": 0.8,
    "patterned": 1.2, "closed_every": 0.9, "corridor": 0.7, "departs_behind": 6,
    "long_cycle": 4,
}
NONCORE_WEIGHT = 4.2   # relative weight of a compound (non-core) root when it applies


@dataclass
class Record:
    seg: g.Segment
    kind: str
    epoch: int
    stratum: str                         # "I" | "II" — PRODUCTION draw (P-STRATA)
    truth: dict = field(default_factory=dict)   # SEALED annotations


#: Share of label objects placed at a node with two or more open departures.
LABEL_AT_JUNCTION = 0.9
#: Chance that a stacked warrant pair is written in the reversed order (hos lekur).
REVERSED_P = 0.45

class Renderer:
    def __init__(self, world: World, core_roots: dict, noncore: dict, seed: int = 1949):
        """core_roots: feature -> root form (sealed key). noncore: form -> (featA, featB)."""
        self.w = world
        self.rng = random.Random(seed)
        self.core = core_roots
        self.noncore = noncore
        self.noncore_by_pair = {}
        for form, pair in noncore.items():
            self.noncore_by_pair.setdefault(frozenset(pair), []).append(form)
        self.forbidden_roots = {"kalsira": 0}     # quota'd uses handled by the planner
        self.suppress: set[str] = set()

    # ------------------------------------------------------------------ roots
    def root_for(self, v: int, e: int, prefer: Optional[str] = None, avoid=()) -> tuple[str, str]:
        feats = self.w.features(v, e)
        if prefer and prefer in feats and prefer in self.core:
            return self.core[prefer], prefer
        cands, weights = [], []
        for f in sorted(feats):
            r = self.core.get(f)
            if r and r not in avoid and r not in self.suppress:
                cands.append((r, f)); weights.append(SALIENCE.get(f, 1))
        fs = sorted(feats)
        for i, a in enumerate(fs):
            for b in fs[i + 1:]:
                for form in self.noncore_by_pair.get(frozenset((a, b)), ()):
                    if form not in avoid:
                        cands.append((form, f"{a}&{b}")); weights.append(NONCORE_WEIGHT)
        if not cands:
            return self.core["still"], "still"
        return self.rng.choices(cands, weights)[0]

    # ------------------------------------------------------------------ pieces
    def _coord(self, link, e, stratum):
        rng = self.rng
        locus = g.GAP
        if rng.random() < 0.22:
            locus = self.root_for(link.actual, e)[0]
        pass_ = rng.choices(("sa", "to", "nu", g.GAP), (0.34, 0.30, 0.22, 0.14))[0]
        if link.sign_varies:
            phase = "nikur"
        else:
            phase = {0: "kihar", 1: "pukal", -1: "rolun"}[link.sign]
        if stratum == "II" and rng.random() < 0.55:
            phase = g.GAP
        elif rng.random() < 0.12:
            phase = g.GAP
        return g.Coordinate(locus, pass_, phase)

    def _warrants(self, made_at: bool, links, e, stratum, stack_quota):
        rng = self.rng
        stable = links and all(len(set(l.status)) == 1 for l in links)
        traversed = links and all(l.traversals[e] > 0 for l in links)
        if rng.random() < 0.07:
            return ["wal"], None
        first = "tir" if made_at else "nes"
        second = "lekur" if stable else ("hos" if not traversed and links else None)
        if stratum == "I" and stack_quota.get("stack", 0) > 0 and rng.random() < 0.55:
            stack_quota["stack"] -= 1
            pair = ["lekur", "hos"]
            kind = "standard"
            if stack_quota.get("reversed", 0) > 0 and rng.random() < REVERSED_P:
                stack_quota["reversed"] -= 1
                pair, kind = ["hos", "lekur"], "reversed"
            return pair, kind
        if second and rng.random() < 0.45:
            return [second], None
        return [first], None

    def _grade(self, link, e):
        rng = self.rng
        if link.status[e] != "open":
            return ("ti", None) if rng.random() < 0.5 else (None, None)
        if link.traversals[e] > 0:
            return "kas", self._discharge(link, e)
        if e + 1 < EPOCHS and link.status[e + 1] == "open" and link.status[e] != "open":
            return "ka", None
        return "lan", self._discharge(link, e)

    def _discharge(self, link, e):
        later = link.status[e:]
        if len(set(later)) == 1:
            return "lun"
        if any(t > 0 for t in link.traversals[e + 1:e + 3]) and "closed" in later:
            return "ro"
        if "closed" in later or "dormant" in later:
            return "sar"
        return "le"

    def _polarity(self, link, e, stratum):
        rng = self.rng
        st = link.status[e]
        pol = {"closed": "sen", "dormant": "nir"}.get(st)
        rs = None
        if pol and rng.random() < 0.42:
            rs = "kur" if link.closed_every or (link.period and pol == "nir") else "li"
        return pol, rs

    # ------------------------------------------------------------------ records
    def route(self, e: int, stratum: str, start: Optional[int] = None, length: Optional[int] = None,
              made_at: Optional[bool] = None, stack_quota=None, grade_p=0.18) -> Optional[Record]:
        rng, w = self.rng, self.w
        length = length or rng.choices((2, 3, 4, 5), (40, 34, 18, 8))[0]
        for _ in range(60):
            v = start if start is not None else rng.randrange(1, len(w.loci))
            path, links = [v], []
            ok = True
            while len(path) < length:
                outs = [l for l in w.out[path[-1]] if l.actual not in path and l.actual != 0]
                if not outs:
                    ok = False
                    break
                l = rng.choice(outs)
                links.append(l)
                path.append(l.actual)
            if ok:
                break
        else:
            return None
        words = []
        used_feats = []
        for i, node in enumerate(path):
            avoid = ()
            if i < len(links):     # the bound pairs are placed by quota, never by accident
                avoid = {"direct": ("kalsira",), "returning": ("lartuki",)}.get(links[i].kind, ())
            root, feat = self.root_for(node, e, avoid=avoid)
            used_feats.append(feat)
            words.append(g.NodeWord(root=root))
        for i, l in enumerate(links):
            cls = KIND_CLASS[l.kind]
            words[i].tail = cls
            words[i + 1].head = cls
            if rng.random() < grade_p:
                gr, dis = self._grade(l, e)
                if gr:
                    words[i].grade = gr
                    if dis and rng.random() < 0.6:
                        words[i].discharge = dis
            if l.status[e] != "open" and rng.random() < 0.5:
                pol, rs = self._polarity(l, e, stratum)
                if pol:
                    words[i].polarity = pol
                    words[i].rscope = rs
                    words[i].scope = stratum == "I"
        # incidence
        words[0].incidence = "in"
        words[-1].incidence = "in"
        for i in range(1, len(words) - 1):
            words[i].incidence = "is" if links[i - 1].kind == "forced" or rng.random() < 0.7 else "ar"
        for i, node in enumerate(path):
            if i in (0, len(path) - 1) and len(w.departures(node, e)) >= 2 and rng.random() < 0.25:
                words[i].incidence = "ar"
        if rng.random() < (0.78 if stratum == "I" else 0.5):
            words[-1].coord = self._coord(links[-1], e, stratum)
        made_at = rng.random() < 0.62 if made_at is None else made_at
        wr, stack = self._warrants(made_at, links, e, stratum, stack_quota or {})
        seg = g.Segment(words, wr)
        return Record(seg, "route", e, stratum, {
            "loci": path, "links": [l.lid for l in links], "features": used_feats,
            "made_at": made_at, "stack": stack})

    def status(self, e: int, stratum: str, stack_quota=None) -> Optional[Record]:
        """One edge and its condition: FRB / UNA / IMP / BAR-described, with or without
        a coordinate."""
        rng, w = self.rng, self.w
        for _ in range(80):
            kind = rng.choices(("closed", "dormant", "imp", "bar"), (38, 26, 14, 22))[0]
            if kind in ("closed", "dormant"):
                pool = [l for l in w.links if l.status[e] == kind and l.src != 0 and l.actual != 0]
                if not pool:
                    continue
                l = rng.choice(pool)
                a, b = self.root_for(l.src, e), self.root_for(l.actual, e)
                cls = KIND_CLASS[l.kind]
                w1 = g.NodeWord(a[0], incidence="in", tail=cls)
                w2 = g.NodeWord(b[0], head=cls, incidence="in")
                pol, rs = self._polarity(l, e, stratum)
                w1.polarity, w1.rscope = pol, rs
                scope_truth = "edge" if rng.random() < 0.86 else "segment"
                w1.scope = stratum == "I" and scope_truth == "edge"
                if rng.random() < (0.55 if stratum == "I" else 0.3):
                    w2.coord = self._coord(l, e, stratum)
                wr, stack = self._warrants(rng.random() < 0.6, [l], e, stratum, stack_quota or {})
                return Record(g.Segment([w1, w2], wr), "status", e, stratum, {
                    "loci": [l.src, l.actual], "links": [l.lid], "features": [a[1], b[1]],
                    "scope": scope_truth, "stack": stack})
            if kind == "imp":
                v = rng.randrange(1, len(w.loci))
                x = rng.randrange(1, len(w.loci))
                if x == v or any(l.actual == x for l in w.out[v]):
                    continue
                a, b = self.root_for(v, e), self.root_for(x, e)
                w1 = g.NodeWord(a[0], incidence="in", tail="PASS", polarity="mun")
                w2 = g.NodeWord(b[0], head="PASS", incidence="in")
                wr, stack = self._warrants(rng.random() < 0.6, [], e, stratum, stack_quota or {})
                return Record(g.Segment([w1, w2], wr), "status", e, stratum, {
                    "loci": [v, x], "links": [], "features": [a[1], b[1]], "imp": True, "stack": stack})
            if kind == "bar":
                pool = [l for l in w.links if l.src != 0 and l.actual != 0 and l.kind != "returning"]
                l = rng.choice(pool)
                a, b = self.root_for(l.actual, e), self.root_for(l.src, e)
                w1 = g.NodeWord(a[0], incidence="in", tail="BAR")
                if len(w.departures(l.actual, e)) >= 2 and rng.random() < 0.5:
                    w1.incidence = "ar"
                w2 = g.NodeWord(b[0], head="BAR", incidence="in")
                if rng.random() < 0.3:
                    w1.polarity = "sen"
                    w1.scope = stratum == "I"
                if rng.random() < 0.5:
                    w2.coord = g.Coordinate(g.GAP, rng.choice(("sa", "nu", "to", g.GAP)), g.GAP)
                wr, stack = self._warrants(rng.random() < 0.55, [l], e, stratum, stack_quota or {})
                return Record(g.Segment([w1, w2], wr), "status", e, stratum, {
                    "loci": [l.actual, l.src], "links": [l.lid], "features": [a[1], b[1]],
                    "bar": True, "scope": "edge", "stack": stack})
        return None

    def label(self, e: int, stratum: str, locus: Optional[int] = None, stack_quota=None) -> Record:
        """A formulaic label: one node word, its incidence, a warrant."""
        rng, w = self.rng, self.w
        if locus is None:
            # label objects mark junctions: that is what the Archive's 1979 reply to Hallam
            # rests on (A §4.6b, "more than a hundred intact Ch-1 objects")
            junctions = [x for x in range(1, len(w.loci)) if len(w.departures(x, e)) >= 2]
            v = rng.choice(junctions) if junctions and rng.random() < LABEL_AT_JUNCTION \
                else rng.randrange(1, len(w.loci))
        else:
            v = locus
        root, feat = self.root_for(v, e)
        junction = len(w.departures(v, e)) >= 2
        inc = "ar" if junction and rng.random() < 0.95 else rng.choice(("in", "in", "ol"))
        wr = [rng.choices(("nes", "tir", "lekur", "hos", "wal"), (40, 30, 14, 8, 8))[0]]
        stack = None
        q = stack_quota or {}
        if stratum == "I" and q.get("stack", 0) > 0 and rng.random() < 0.4:
            q["stack"] -= 1
            wr, stack = ["lekur", "hos"], "standard"
            if q.get("reversed", 0) > 0 and rng.random() < REVERSED_P:
                q["reversed"] -= 1
                wr, stack = ["hos", "lekur"], "reversed"
        return Record(g.Segment([g.NodeWord(root, incidence=inc)], wr), "label", e, stratum, {
            "loci": [v], "links": [], "features": [feat], "junction": junction, "stack": stack})

    def authorization(self, e: int, stratum: str, unent: bool = False) -> Optional[Record]:
        rng, w = self.rng, self.w
        if unent:
            pool = [l for l in w.links if l.status[e] == "closed" and l.src != 0 and l.actual != 0]
        else:
            pool = [l for l in w.links if l.status[e] == "open" and l.src != 0 and l.actual != 0]
        if not pool:
            return None
        l = rng.choice(pool)
        a, b = self.root_for(l.src, e), self.root_for(l.actual, e)
        cls = KIND_CLASS[l.kind]
        if unent:
            gr, dis = rng.choice(("lan", "kas")), rng.choice(("lun", "sar", "le"))
        else:
            gr, dis = self._grade(l, e)
            gr = gr or "lan"
        w1 = g.NodeWord(a[0], incidence="in", tail=cls, grade=gr, unent=unent, discharge=dis)
        w2 = g.NodeWord(b[0], head=cls, incidence="in", coord=self._coord(l, e, stratum))
        wr = [rng.choice(("nes", "tir"))]
        return Record(g.Segment([w1, w2], wr), "authorization", e, stratum, {
            "loci": [l.src, l.actual], "links": [l.lid], "features": [a[1], b[1]],
            "open_register": gr == "lan" and dis == "lun", "unent": unent})

    def bind(self, e: int, stratum: str) -> Record:
        rng, w = self.rng, self.w
        v = rng.randrange(1, len(w.loci))
        a = self.root_for(v, e)
        b = self.root_for(v, e, avoid=(a[0],))
        w1 = g.NodeWord(a[0], incidence="in", tail="BIND")
        w2 = g.NodeWord(b[0], head="BIND", incidence="ol",
                        coord=g.Coordinate(g.GAP, "sa", "kihar") if rng.random() < 0.6 else None)
        return Record(g.Segment([w1, w2], [rng.choice(("tir", "nes", "hos"))]), "bind", e, stratum, {
            "loci": [v, v], "links": [], "features": [a[1], b[1]]})

    def shadow(self, e: int, stratum: str) -> Optional[Record]:
        """P-SHADOW: a SIM-graded edge onto an OFF node. No truth value."""
        rng, w = self.rng, self.w
        pool = [l for l in w.links if l.status[e] != "open" and l.src != 0 and l.actual != 0]
        if not pool:
            return None
        l = rng.choice(pool)
        a, b = self.root_for(l.src, e), self.root_for(l.actual, e)
        cls = KIND_CLASS[l.kind]
        w1 = g.NodeWord(a[0], incidence="in", tail=cls, grade="ti")
        w2 = g.NodeWord(b[0], head=cls, incidence="ol")
        return Record(g.Segment([w1, w2], [rng.choice(("hos", "nes"))]), "shadow", e, stratum, {
            "loci": [l.src, l.actual], "links": [l.lid], "features": [a[1], b[1]], "production": "P-SHADOW"})

    def half_negation(self, e: int, stratum: str) -> Record:
        """A tail with IMP and no destination: 'departure is impossible' or 'no such
        departure exists' — undecided (A §4.4)."""
        rng, w = self.rng, self.w
        sinks = [v for v in range(1, len(w.loci)) if not w.out[v]]
        v = rng.choice(sinks)
        a = self.root_for(v, e)
        w1 = g.NodeWord(a[0], incidence="in", tail=rng.choice(("PASS", "PASS", "THRU")), polarity="mun")
        return Record(g.Segment([w1], [rng.choice(("tir", "nes", "hos"))]), "half-negation", e, stratum, {
            "loci": [v], "links": [], "features": [a[1]], "sink": True})

    def kalsira_ru(self, e: int, completed: bool, stratum: str) -> Optional[Record]:
        """The bound pair (A §10.1a). Frozen where a held coordinate has no direct
        departure; compositional (Stratum I only) where it has one."""
        rng, w = self.rng, self.w
        held = [v for v in range(1, len(w.loci)) if w.loci[v].dwell]
        if completed:
            cands = [(v, l) for v in held for l in w.out[v] if l.kind == "direct" and l.actual != 0]
            if not cands:
                return None
            v, l = rng.choice(cands)
            b = self.root_for(l.actual, e)
            w1 = g.NodeWord("kalsira", incidence="in", tail="PASS")
            w2 = g.NodeWord(b[0], head="PASS", incidence="in", coord=self._coord(l, e, "I"))
            wr = ["tir", "lekur"]
            return Record(g.Segment([w1, w2], wr), "kalsira-ru", e, "I", {
                "loci": [v, l.actual], "links": [l.lid], "features": ["held", b[1]], "pair": "compositional"})
        cands = [v for v in held if not any(l.kind == "direct" for l in w.out[v])]
        v = rng.choice(cands)
        prev = [l for l in w.inn[v] if l.src != 0]
        words = []
        if prev and rng.random() < 0.7:
            l0 = rng.choice(prev)
            a = self.root_for(l0.src, e, avoid=("kalsira",))
            cls = KIND_CLASS[l0.kind]
            words.append(g.NodeWord(a[0], incidence="in", tail=cls))
            words.append(g.NodeWord("kalsira", head=cls, tail="PASS"))
        else:
            words.append(g.NodeWord("kalsira", tail="PASS"))
        wr = [rng.choice(("tir", "nes", "hos"))]
        return Record(g.Segment(words, wr), "kalsira-ru", e, stratum, {
            "loci": [v], "links": [], "features": ["held"], "pair": "frozen"})

    def lartuki_halu(self, e: int, stratum: str) -> Optional[Record]:
        """The bound pair nothing turns on (A §10.1b): coordinate hilun-nu-hilun in every one."""
        rng, w = self.rng, self.w
        per = [v for v in range(1, len(w.loci)) if w.out[v] and all(l.period for l in w.out[v])]
        v = rng.choice(per)
        prev = [l for l in w.inn[v] if l.src != 0] or [None]
        l0 = rng.choice(prev)
        if l0 is None:
            return None
        a = self.root_for(l0.src, e, avoid=("lartuki",))
        cls = KIND_CLASS[l0.kind]
        w1 = g.NodeWord(a[0], incidence="in", tail=cls)
        w2 = g.NodeWord("lartuki", head=cls, incidence="in", tail="RECUR",
                        coord=g.Coordinate(g.GAP, "nu", g.GAP))
        return Record(g.Segment([w1, w2], [rng.choice(("tir", "nes"))]), "lartuki-halu", e, stratum, {
            "loci": [l0.src, v], "links": [l0.lid], "features": [a[1], "periodic"],
            "pair": "frozen", "period_exceeds_span": True})
