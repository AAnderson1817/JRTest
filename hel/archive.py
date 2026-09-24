"""The Archive: transcription, catalogue, and the published figures.

Authority C. This module plays HEL. It receives damaged records and does to them
exactly what the documents say HEL's institutions did — including the errors — and
it computes every figure the Archive publishes from the catalogue it builds. Nothing
here reads truth: transcription works on the damaged record's surface, and the only
sealed things it touches are the pointers it carries through for ``hel.export`` to
strip.

The 1908 procedure, as implemented:

* **The Stratum II cut.** Where the destination root is vowel-initial, the trace gives
  no separation between the arrival flick and the root's opening vowel, and the
  committee ruled the head half absent (A §7.1). The rule is applied; whether it is
  right is P-SEGMENTATION and has no answer here.
* **Illegible intervals** are transcribed ADJ, tail half only — the register clerks'
  mark, consolidated as a class in 1908 and kept by the Standard since (A §4.6c).
* **Hand copies** (Ch-2 before photography): copyists confused the /h/–/k/ forms the
  code cannot tell apart (A §6.1b), and marked a page break with the junction sign.
"""
from __future__ import annotations

import random
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Optional

from . import grammar as g
from . import phonology as ph

VOWEL_INITIAL = lambda root: root[:1] in "aeiou"
HK = {"ha": "ka", "ka": "ha", "he": "ke", "ke": "he", "hi": "ki", "ki": "hi"}


@dataclass
class Entry:
    cid: str
    channel: str
    stratum: str
    source: str                     # object | plate | hand copy | log | recitation
    locus: Optional[str]
    accession_year: Optional[int]
    catalogued_year: int
    condition: str
    segments: list = field(default_factory=list)     # catalogued g.Segment
    units: list = field(default_factory=list)        # III / IV / field sequence
    notes: list = field(default_factory=list)
    register: dict = field(default_factory=dict)     # pre-1908 register collation
    field_name: Optional[str] = None
    expedition: Optional[str] = None
    iii_position: Optional[str] = None
    obj: str = ""                                    # the physical object (entries may share one)
    part: str = ""                                   # "" or "III" for a field on a traced object
    sealed: dict = field(default_factory=dict)       # SEALED pointers; stripped on export

    @property
    def ref(self) -> str:
        return self.cid + (f"/{self.part}" if self.part else "")

    def transliteration(self) -> str:
        parts = [s.translit() for s in self.segments]
        if self.units:
            parts.append(" · ".join(self.units))
        return "  ‖  ".join(parts)

    def tokens(self) -> list[str]:
        out = []
        for s in self.segments:
            out += s.tokens()
        return out + list(self.units)


def transcribe(rec, *, channel: str, source: str, pre1908: bool, rng: random.Random,
               copy_generations: int = 0) -> tuple[g.Segment, dict]:
    """Apply the Standard to one damaged record. Returns the catalogued segment and a
    notes dict (register collation, environments, copy errors)."""
    import copy as _copy
    seg = _copy.deepcopy(rec.seg)
    notes = {"env": [], "adj": 0, "copy": [], "page_end_ar": False}
    ws = seg.words
    # illegible intervals -> ADJ tail; the head is never read
    for i, w in enumerate(ws):
        if getattr(w, "tail_illegible", False):
            w.tail = "ADJ"
            w.grade = w.polarity = w.rscope = w.discharge = None
            w.scope = w.unent = False
            notes["adj"] += 1
        if getattr(w, "head_illegible", False):
            w.head = None
            if w.coord is not None:
                pass   # the carrier lost its head: the coordinate is kept and unreadable
    # the Stratum II cut before vowel-initial roots
    if rec.stratum == "II":
        for i in range(len(ws) - 1):
            a, b = ws[i], ws[i + 1]
            if a.tail and b.head and a.tail == b.head and VOWEL_INITIAL(b.root):
                if b.coord is not None:
                    # Engine finding F-07. The cut rule and A §4.3's distribution fact
                    # ("100% of coordinate-bearing words are head-bearing") collide here.
                    # The committee's tie-break: a cartouche after the cluster proves an
                    # edge arrives, so the head is ruled present. The 100% figure is
                    # therefore partly the committee's own rule.
                    notes.setdefault("cartouche_tiebreak", 0)
                    notes["cartouche_tiebreak"] += 1
                    continue
                short = rng.random() < 0.43                   # notch count too low for a head
                env = {"root": b.root, "ch1": channel == "Ch-1", "trace": "short" if short else "indeterminate"}
                if pre1908 and not short:
                    env["older_branch_cut"] = "present" if rng.random() < 0.365 else "absent"
                notes["env"].append(env)
                b.head = None
    # hand copies
    if source == "hand copy":
        for gen in range(copy_generations):
            for w in ws:
                sy = list(ph.syllables(w.root))
                for k, s in enumerate(sy):
                    if s in HK and rng.random() < 0.035:
                        sy[k] = HK[s]
                        notes["copy"].append((w.root, "".join(sy)))
                w.root = "".join(sy)
        if len(ws) >= 2 and rng.random() < 0.33:
            k = rng.randrange(len(ws) - 1)
            if ws[k].incidence != "ar":
                ws[k].incidence = "ar"
                notes["page_end_ar"] = True
    return seg, notes


# --- the published figures -------------------------------------------------------


def figures(entries: list[Entry], lex_forms: dict) -> dict:
    """Everything the Archive publishes about its own catalogue, computed."""
    F = {}
    toks_by = Counter()
    strat_tokens = Counter()
    all_tokens = []
    functional = []
    for e in entries:
        t = e.tokens()
        all_tokens += t
        toks_by[e.channel] += len(t)
        strat_tokens[e.stratum.split(" ")[0]] += len(t)
        if e.stratum.split(" ")[0] in ("I", "II"):
            functional += t
    n = len(all_tokens)
    F["tokens"] = n
    F["channel_share"] = {k: round(v / n, 3) for k, v in sorted(toks_by.items())}
    F["stratum_share"] = {k: round(v / n, 3) for k, v in sorted(strat_tokens.items())}
    F["stratum_tokens"] = dict(strat_tokens)
    # sequences: each catalogued segment / field is a sequence
    seqs = []
    for e in entries:
        for s in e.segments:
            seqs.append(s.tokens())
        if e.units:
            seqs.append(list(e.units))
    F["sequences"] = len(seqs)
    F["tokens_in_seq_ge3"] = sum(len(s) for s in seqs if len(s) >= 3)
    F["longest_sequence"] = max(len(s) for s in seqs)
    F["sequences_over_30"] = sum(len(s) > 30 for s in seqs)
    # functional types (I-II), by sequence occurrence
    occ = defaultdict(set)
    cnt = Counter()
    k = 0
    for e in entries:
        if e.stratum.split(" ")[0] not in ("I", "II"):
            continue
        for s in e.segments:
            k += 1
            for t in s.tokens():
                occ[t].add(k)
                cnt[t] += 1
    F["functional_types"] = len(cnt)
    F["functional_types_gt5"] = sum(c > 5 for c in cnt.values())
    F["functional_seq_hapax"] = sum(len(v) == 1 for v in occ.values())
    # broken halves
    term_broken = 0
    fsegs = [s for e in entries for s in e.segments]
    for s in fsegs:
        es = g.edges_of(s)
        last = len(s.words) - 1
        if any(x.kind == "broken-tail" and x.origin == last for x in es) or \
           any(x.kind == "broken-head" and x.dest == 0 for x in es):
            term_broken += 1
    F["functional_segments"] = len(fsegs)
    F["segments_ending_in_broken_half"] = term_broken
    F["broken_share"] = round(term_broken / max(1, len(fsegs)), 3)
    # warrants
    stacked = [s.warrants for s in fsegs if len(s.warrants) > 1]
    F["stacked_warrants"] = len(stacked)
    F["stacked_reversed"] = sum(1 for w in stacked if w[0] == "hos")
    # half-negated tails
    F["tail_only_mun"] = sum(1 for s in fsegs for x in g.edges_of(s)
                             if x.kind == "broken-tail" and s.words[x.origin].polarity == "mun")
    # the bound pairs
    kr = [(e, s) for e in entries for s in e.segments for w in s.words if w.root == "kalsira" and w.tail == "PASS"]
    F["kalsira_ru"] = {
        "total": len(kr),
        "completed_I": sum(1 for e, s in kr if e.stratum == "I" and _completed(s, "kalsira")),
        "uncompleted": sum(1 for e, s in kr if not _completed(s, "kalsira")),
        "uncompleted_by_stratum": dict(Counter(e.stratum for e, s in kr if not _completed(s, "kalsira"))),
    }
    F["lartuki_halu"] = sum(1 for s in fsegs for w in s.words if w.root == "lartuki" and w.tail == "RECUR")
    # multi-edge coordinates (where the Standard and Sturge come apart)
    multi = 0
    for s in fsegs:
        for j, w in enumerate(s.words):
            if w.coord is not None:
                into = [x for x in g.edges_of(s) if x.dest == j and x.kind == "complete"]
                if into and into[0].origin is not None and any(
                        y.dest == into[0].origin and y.kind == "complete" for y in g.edges_of(s)):
                    multi += 1
    F["multi_edge_coordinate_segments"] = multi
    # SHUNT / RECUR attestations
    F["shunt_recur_edges"] = sum(1 for s in fsegs for x in g.edges_of(s) if x.cls in ("SHUNT", "RECUR"))
    F["adj_halves"] = sum(1 for s in fsegs for w in s.words if w.tail == "ADJ")
    F["adj_pairs"] = sum(1 for s in fsegs for x in g.edges_of(s) if x.cls == "ADJ" and x.kind == "complete")
    # the junction map: HEL identifies a node by (find locus, root)
    jmap = defaultdict(lambda: {"ar": False, "departures": set()})
    for e in entries:
        for s in e.segments:
            for x in g.edges_of(s):
                if x.origin is not None and x.dest is not None:
                    jmap[(e.locus, s.words[x.origin].root)]["departures"].add(s.words[x.dest].root)
            for w in s.words:
                if w.incidence == "ar":
                    jmap[(e.locus, w.root)]["ar"] = True
    junctions = {k: v for k, v in jmap.items() if v["ar"] or len(v["departures"]) >= 2}
    F["junction_map_nodes"] = len(junctions)
    F["junction_by_ar_only"] = sum(1 for v in junctions.values() if v["ar"] and len(v["departures"]) < 2)
    # the Stratum II environment
    envs = [x for e in entries for x in e.register.get("env", [])]
    F["stratum_II_env"] = {
        "total": len(envs),
        "ch1": sum(x["ch1"] for x in envs),
        "ch1_short": sum(x["ch1"] and x["trace"] == "short" for x in envs),
        "ch1_undetermined": sum(x["ch1"] and x["trace"] == "indeterminate" for x in envs),
        "ch1_undetermined_with_register": sum(x["ch1"] and "older_branch_cut" in x for x in envs),
        "older_branch_cut_present": sum(x.get("older_branch_cut") == "present" for x in envs),
    }
    # coda and syllable profile, by class
    def prof(tokens):
        ts = [t for t in tokens if t != "[41]"]
        cod = sum(ph.is_closed(ph.syllables(t)[-1]) or ph.syllables(t)[-1] in ph.ONSETLESS for t in ts)
        syl = sum(len(ph.syllables(t)) for t in ts)
        return {"coda_final_share": round(cod / max(1, len(ts)), 3), "mean_syllables": round(syl / max(1, len(ts)), 2)}
    F["profile_functional"] = prof(functional)
    iii_tokens = [t for e in entries if e.stratum.startswith("III") for t in e.units]
    F["profile_III"] = prof(iii_tokens)
    F["open_register"] = sum(1 for s in fsegs for w in s.words if w.grade == "lan" and w.discharge == "lun")
    F["unentitled"] = sum(1 for s in fsegs for w in s.words if w.unent)
    F["shadow_parses"] = sum(1 for s in fsegs for x in g.edges_of(s)
                             if x.origin is not None and x.dest is not None
                             and s.words[x.origin].grade == "ti" and s.words[x.dest].incidence == "ol")
    F["imports"] = {
        "H1_discharge": sum(1 for s in fsegs for w in s.words if w.discharge),
        "H2_unent": F["unentitled"],
        "H3_rscope": sum(1 for s in fsegs for w in s.words if w.rscope),
    }
    return F


def _completed(seg, root):
    for x in g.edges_of(seg):
        if x.origin is not None and seg.words[x.origin].root == root and x.cls == "PASS":
            return x.kind == "complete"
    return False


def iii_figures(entries: list[Entry]) -> dict:
    """A-reserve §4, computed."""
    seqs = [e for e in entries if e.stratum.startswith("III")]
    F = {"sequences": len(seqs), "tokens": sum(len(e.units) for e in seqs)}
    lens = [len(e.units) for e in seqs]
    F["mean_length"] = round(sum(lens) / max(1, len(lens)), 1)
    F["length_range"] = (min(lens), max(lens)) if lens else None
    F["divisible_by_three"] = sum(l % 3 == 0 for l in lens)
    occ = defaultdict(set)
    within = []
    for i, e in enumerate(seqs):
        c = Counter(e.units)
        for t, k in c.items():
            occ[t].add(i)
            within.append(k >= 2)
    F["types"] = len(occ)
    F["types_in_one_sequence"] = sum(len(v) == 1 for v in occ.values())
    F["p_recur_within"] = round(sum(within) / max(1, len(within)), 2)
    pairs = [(i, t) for i, e in enumerate(seqs) for t in set(e.units)]
    F["p_recur_elsewhere"] = round(sum(len(occ[t]) > 1 for _, t in pairs) / max(1, len(pairs)), 2)
    F["channel"] = dict(Counter(e.channel for e in seqs))
    F["position"] = dict(Counter(e.iii_position for e in seqs))
    F["find_loci"] = len({e.locus for e in seqs if e.locus})
    F["provisional"] = sum(e.stratum == "III (provisional)" for e in seqs)
    return F
