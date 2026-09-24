"""The internal grammar of Architecture A′ as a program (Phase 2 plan item 4).

Authority C. Implements A §4–§5 and the four Phase 1 imports (H1–H3 are grammar;
H4 is the attrition model in ``hel.taphonomy``). Every formative carries the
Archive's confidence grade and its standing challenge, because the grammar is
itself a reconstruction (A §4 preamble).

The template (A §4.3, extended by H1–H3):

    [HEAD-] ROOT [-INC] [-TAIL] [-GRADE [-UNENT] [-DISCH]] [-POL [-RSCOPE]] [-SCOPE] [=COORD]

A segment is a chain of node words joined by bipartite edges and closed by one or
more warrants; Ch-4 formulae may carry ritual-only free units before the warrant.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Optional

from . import phonology as ph

# --- inventory ----------------------------------------------------------------


@dataclass(frozen=True)
class Formative:
    form: str
    abbr: str
    slot: str
    meaning: str
    grade: str
    challenge: str
    cls: Optional[str] = None
    imported: Optional[str] = None  # "H1" / "H2" / "H3" for the A′ imports


EDGE_CLASSES = {
    # class: (tail, head, gloss, grade, challenge)
    "PASS": ("ru", "ru", "sanctioned direct traversal", "G2",
             "Most frequent class; a century of route outcomes consistent with the reading. "
             "Nothing verifies that 'sanctioned' is in the record rather than in HEL"),
    "THRU": ("ken", "ke", "leg of a forced multi-node path", "G2",
             "Validated by the broken-half method; 'forced' is inferred from the absence of "
             "a co-attested direct edge, not stated"),
    "SHUNT": ("tul", "tu", "arrival displaced from intent", "G3",
              "May be one class with RECUR, split by the 1908 consolidation (A §4.6a)"),
    "BAR": ("pel", "pe", "edge present in the graph, not traversable in this orientation", "G2",
            "Secure against IMP since the 1948 revision"),
    "RECUR": ("halu", "ha", "return to a similar but non-identical coordinate", "G3",
              "May be one class with SHUNT (A §4.6a)"),
    "BIND": ("sil", "si", "co-incidence: same coordinate under two descriptions; not motion", "G1",
             "No expedition outcome distinguishes a true BIND claim from a false one"),
    "ADJ": ("yun", "yu", "adjacency attested, orientation unrecovered", "G3",
            "May be a nineteenth-century damage convention, not a class (A §4.6c). "
            "No head half has ever been recovered; yu- is derived by rule"),
}
MOTION_CLASSES = ("PASS", "THRU", "SHUNT", "BAR", "RECUR", "ADJ")

_F = []
for _c, (_t, _h, _g, _gr, _ch) in EDGE_CLASSES.items():
    _F.append(Formative(_t, f"{_c}.TAIL", "tail", _g, _gr, _ch, cls=_c))
    _F.append(Formative(_h, f"{_c}.HEAD", "head", _g, _gr, _ch, cls=_c))

_F += [
    Formative("in", "TERM", "incidence", "endpoint of the chain", "G2",
              "'Endpoint of the chain' vs 'endpoint of the record' is not distinguishable"),
    Formative("is", "MED", "incidence", "traversed through", "G2",
              "Validated jointly with THRU; almost never independently testable"),
    Formative("ar", "JCT", "incidence", "other edges attach here, not stated", "G3",
              "May mark that the record is incomplete here (Hallam 1976, A §4.6b)"),
    Formative("ol", "OFF", "incidence", "referenced, not on this path", "G1",
              "'Referenced' imports a referring act; nothing operational turns on OFF"),
    Formative("ti", "SIM", "grade", "modeled; no commitment", "G1",
              "A modeled traversal produces no outcome to correlate against"),
    Formative("ka", "PREP", "grade", "staged; conditions being brought into place", "G1",
              "The Archive's paraphrase of a contrast, not of anything the corpus states"),
    Formative("lan", "AUTH", "grade", "authorized", "G3",
              "Performative ('I hereby authorize') vs stative ('in an authorized state'); "
              "Field Protocol restricts speaking AUTH forms near an active locus"),
    Formative("kas", "EXEC", "grade", "executed or executing", "G2",
              "Best-correlated grade; completed vs in-progress is not recoverable"),
    Formative("mun", "IMP", "polarity", "the edge does not exist in the graph", "G2", ""),
    Formative("sen", "FRB", "polarity", "the edge exists and is traversable, and is closed", "G3",
              "By whom or by what is not stated; the Instrument school reads 'gated'"),
    Formative("nir", "UNA", "polarity", "exists, not closed, not available at this coordinate", "G2",
              "Whether dormancy is periodic, conditional or permanent is not stated"),
    Formative("lus", "UNV", "polarity", "this record does not establish the edge's status", "G1",
              "An asserted absence; conflated with wal UNW until 1948"),
    Formative("he", "SCOPE", "scope", "polarity attaches to the edge pair, not the segment", "G1",
              "Function inferred from the ambiguity its absence produces elsewhere"),
    # --- A′ import H2: the unentitled-grade marker (Phase 1 §4.4) ---
    Formative("lar", "UNENT", "unent", "grade taken without entitlement", "G3",
              "Utterance: performed without entitlement. Instrument: recorded with the "
              "permission bit clear. Glossed dual-read at point of use; no first-person "
              "paraphrase", imported="H2"),
    # --- A′ import H1: discharge on graded edges ---
    Formative("ro", "SPENT", "discharge", "the grade has been discharged", "G1",
              "No outcome distinguishes a spent grade from a lapsed one", imported="H1"),
    Formative("lun", "STANDING", "discharge", "the grade remains in force; no release recorded", "G3",
              "Performative (in force until remitted) vs stative (a lifetime flag). "
              "AUTH-STANDING with no attested release is the Open Register", imported="H1"),
    Formative("ki", "COND", "discharge", "in force under a condition the record does not state", "G1",
              "The condition is never stated; the value is known only by contrast",
              imported="H1"),
    Formative("sar", "LAPSED", "discharge", "ceased without discharge", "G1",
              "Distinguished from SPENT by paradigm position only", imported="H1"),
    Formative("le", "DISCH.GAP", "discharge", "discharge not stated, and the record says so", "G2",
              "Formally clean; the overt-gap principle applied to discharge", imported="H1"),
    # --- A′ import H3: recurrence scope on polarity ---
    Formative("li", "ONCE", "rscope", "the polarity holds at this pass", "G2",
              "Edges closed ONCE have been found open on later passes", imported="H3"),
    Formative("kur", "EVERY", "rscope", "the polarity holds at every recurrence", "G2",
              "No EVERY-closed edge has been found open; absence of a counterexample", imported="H3"),
    Formative("ra", "RSCOPE.GAP", "rscope", "recurrence scope not stated", "G1",
              "An explicit negative value; cannot be validated", imported="H3"),
    # --- warrants (A §4.5) ---
    Formative("nes", "REG", "warrant", "entered without a human attestor", "G2",
              "Formerly glossed 'registered by the system itself'; struck 1949"),
    Formative("tir", "WIT", "warrant", "attested at the locus", "G2",
              "The most human-shaped warrant; Instrument reads a sensor-provenance field"),
    Formative("lekur", "REP", "warrant", "held on multiple passes", "G2",
              "The lekur-alone rule: never translated with 'because'"),
    Formative("hos", "INF", "warrant", "derived structurally from other edges", "G1",
              "An inferred route successfully traversed confirms the route, not the inference"),
    Formative("wal", "UNW", "warrant", "no source carried", "G1",
              "Rests entirely on contrast with the other four; conflated with lus until 1948"),
    Formative("[41]", "41", "warrant", "a sixth unit in the warrant slot; no sound value assigned",
              "G5", "Transmitted, not analyzed. Never eliminated as a copyist's artifact. "
              "Must not be explained"),
    # --- coordinate (A §5.2) ---
    Formative("sa", "PASS.SAME", "pass", "same pass", "G2",
              "Correlates with records HEL can independently date to one traversal"),
    Formative("to", "PASS.LATER", "pass", "a later pass", "G2",
              "The one ordering claim operational records can check"),
    Formative("nu", "PASS.OTHER", "pass", "another pass, ordering unrecovered", "G1",
              "Indistinguishable from a default written when a field was not filled"),
    Formative("kihar", "PHASE.SAME", "phase", "at the anchor; no displacement stated", "G2",
              "The unmarked, best-attested value"),
    Formative("pukal", "PHASE.AHEAD.MEAS", "phase",
              "displaced ahead of the anchor, measured; the magnitude is not in the record", "G3",
              "'Measured' is inferred from nikur's existence (A §5.2, §5.2b)"),
    Formative("rolun", "PHASE.BEHIND.MEAS", "phase",
              "displaced behind the anchor, measured; the magnitude is not in the record", "G3",
              "As pukal"),
    Formative("nikur", "PHASE.DISP.UNMEAS", "phase", "displaced, unmeasured", "G3",
              "Instrument: purely qualitative 'unresolved'"),
    Formative("hilun", "GAP", "gap", "this slot is unfilled, and the record says so", "G2",
              "'Unknown to the record' vs 'withheld by the record' has never been settled"),
]
FORMATIVES = tuple(_F)

HEADS = {f.form: f for f in FORMATIVES if f.slot == "head"}
TAILS = {f.form: f for f in FORMATIVES if f.slot == "tail"}
BY_SLOT = {}
for _f in FORMATIVES:
    if _f.slot not in ("head", "tail"):
        BY_SLOT.setdefault(_f.slot, {})[_f.form] = _f
INCIDENCE = BY_SLOT["incidence"]
GRADES = BY_SLOT["grade"]
UNENT = BY_SLOT["unent"]
DISCHARGE = BY_SLOT["discharge"]
POLARITY = BY_SLOT["polarity"]
RSCOPE = BY_SLOT["rscope"]
SCOPE = BY_SLOT["scope"]
WARRANTS = BY_SLOT["warrant"]
PASS_VALUES = BY_SLOT["pass"]
PHASE_VALUES = BY_SLOT["phase"]
GAP = "hilun"

#: A §4 preamble counts thirty-five graded formatives and slot values: the seven
#: classes (not fourteen halves), incidence, grade, polarity, scope, the six
#: warrant-slot units, the LOCUS root filler, PASS, PHASE and the gap marker.
A_PREAMBLE_ITEMS = (
    [(c, EDGE_CLASSES[c][3]) for c in EDGE_CLASSES]
    + [(f.abbr, f.grade) for s in ("incidence", "grade", "polarity", "scope", "warrant",
                                     "pass", "phase", "gap") for f in BY_SLOT[s].values()]
    + [("LOCUS(root)", "G1")]
)

SUFFIX_ORDER = ("incidence", "tail", "grade", "unent", "discharge", "polarity", "rscope", "scope")


def abbr_q(f: Formative) -> str:
    """Interlinear abbreviation; G3 formatives carry '?' (A §6.3)."""
    return f.abbr + ("?" if f.grade == "G3" else "")


# --- data model -------------------------------------------------------------------


@dataclass
class Coordinate:
    locus: Optional[str] = GAP
    pass_: Optional[str] = GAP
    phase: Optional[str] = GAP

    def slots(self):
        return (self.locus, self.pass_, self.phase)

    def translit(self) -> str:
        return "-".join("" if s is None else s for s in self.slots())


@dataclass
class NodeWord:
    root: str
    head: Optional[str] = None        # edge class
    incidence: Optional[str] = None   # form: in / is / ar / ol
    tail: Optional[str] = None        # edge class
    grade: Optional[str] = None       # form
    unent: bool = False
    discharge: Optional[str] = None   # form
    polarity: Optional[str] = None    # form
    rscope: Optional[str] = None      # form
    scope: bool = False
    coord: Optional[Coordinate] = None
    tail_illegible: bool = False      # layer-1 damage: the flick survives, unclassable
    head_illegible: bool = False

    def morphemes(self) -> list[tuple[str, str]]:
        """(slot, form) in surface order."""
        m = []
        if self.head:
            m.append(("head", EDGE_CLASSES[self.head][1]))
        m.append(("root", self.root))
        if self.incidence:
            m.append(("incidence", self.incidence))
        if self.tail:
            m.append(("tail", EDGE_CLASSES[self.tail][0]))
        if self.grade:
            m.append(("grade", self.grade))
        if self.unent:
            m.append(("unent", "lar"))
        if self.discharge:
            m.append(("discharge", self.discharge))
        if self.polarity:
            m.append(("polarity", self.polarity))
        if self.rscope:
            m.append(("rscope", self.rscope))
        if self.scope:
            m.append(("scope", "he"))
        return m

    def translit(self) -> str:
        s = "-".join(f for _, f in self.morphemes())
        if self.coord is not None:
            s += "=" + self.coord.translit()
        return s


@dataclass
class Segment:
    words: list[NodeWord]
    warrants: list[str] = field(default_factory=list)
    free: list[str] = field(default_factory=list)   # Ch-4 ritual-only units

    def translit(self) -> str:
        parts = [w.translit() for w in self.words] + list(self.free)
        if self.warrants:
            parts.append(" ".join(self.warrants))
        return " · ".join(parts)

    def tokens(self) -> list[str]:
        """Catalogued unit tokens: every morpheme, filler, free unit and warrant."""
        out = []
        for w in self.words:
            out += [f for _, f in w.morphemes()]
            if w.coord is not None:
                out += [s for s in w.coord.slots() if s is not None]
        return out + list(self.free) + list(self.warrants)


# --- well-formedness --------------------------------------------------------------


@dataclass
class Finding:
    code: str
    severity: str      # "ill-formed" | "damaged" | "note"
    where: str
    message: str


@dataclass(frozen=True)
class Edge:
    origin: Optional[int]   # index of the tail-bearing word
    dest: Optional[int]     # index of the head-bearing (or implied) destination word
    cls: str
    kind: str               # complete | reduced | broken-tail | broken-head | mismatch


def edges_of(seg: Segment) -> list[Edge]:
    """Pair edge halves between adjacent words.

    *complete* — tail and head of one class on adjacent words, in either linear
    order: the trace reads from either end and so does a Stratum I chain (A §3.5).

    *reduced* — a tail whose next word bears no head: the Stratum II profile.
    **Engine finding F-04:** with the head gone, the transliteration no longer says
    which neighbour the edge enters. The trace does (the departure flick points), so
    the Standard resolves it by convention — every chain is transcribed from its
    first tail-bearer — and a reduced edge enters the *next* word. Orientation-
    invariant reading is therefore a property of the trace and of Stratum I; a
    Stratum II transliteration depends on the committee's writing direction.

    *broken* — a half at a chain margin with nothing to pair with: damage
    (``-ken ⌀``), or a lexicalized bound pair the Archive has not yet identified
    (A §4.2: the two are formally indistinguishable).
    """
    ws = seg.words
    n = len(ws)
    out: list[Edge] = []
    tail_used, head_used = [False] * n, [False] * n
    for i in range(n - 1):
        a, b = ws[i], ws[i + 1]
        if a.tail and b.head and not tail_used[i] and not head_used[i + 1]:
            kind = "complete" if a.tail == b.head else "mismatch"
            out.append(Edge(i, i + 1, a.tail, kind))
            tail_used[i] = head_used[i + 1] = True
        elif a.head and b.tail and not head_used[i] and not tail_used[i + 1] and a.head == b.tail:
            out.append(Edge(i + 1, i, b.tail, "complete"))
            tail_used[i + 1] = head_used[i] = True
    for i in range(n - 1):
        if ws[i].tail and not tail_used[i] and not ws[i + 1].head:
            out.append(Edge(i, i + 1, ws[i].tail, "reduced"))
            tail_used[i] = True
    for k, w in enumerate(ws):
        if w.tail and not tail_used[k]:
            out.append(Edge(k, None, w.tail, "broken-tail"))
        if w.head and not head_used[k]:
            out.append(Edge(None, k, w.head, "broken-head"))
    return out


def construction(w) -> Optional[tuple[str, str]]:
    """The tail-only forms the Archive has identified as constructions rather than damage.
    They present exactly like a broken half (-TAIL ⌀) and are catalogued as what they are.
    (Found by the blind trial: the first Phase 2 engine flagged them D-BROKEN, sixty years
    after Keele. The nine pairs HEL has not identified are still flagged: that is the
    re-audit nobody has run.)"""
    if w.root == "kalsira" and w.tail == "PASS":
        return "N-PAIR", "the bound pair kalsira-ru: the tail projects no edge (Keele 1963, A §10.1a)"
    if w.root == "lartuki" and w.tail == "RECUR":
        return "N-PAIR", "the bound pair lartuki-halu (the 1969 paraphrase, A §10.1b)"
    if w.polarity == "mun" and w.tail:
        return "N-HALFNEG", "-mun on the tail half alone: a half-negated edge (A §4.4)"
    return None


def check(seg: Segment, channel: str = "Ch-1") -> list[Finding]:
    f: list[Finding] = []
    ws = seg.words
    edges = edges_of(seg)
    by_origin = {e.origin: e for e in edges if e.origin is not None}
    for k, w in enumerate(ws):
        where = f"word {k + 1} ({w.root})"
        if (w.grade or w.polarity or w.unent or w.discharge or w.rscope or w.scope) and not w.tail:
            f.append(Finding("E-EDGELESS", "ill-formed", where,
                             "grade and polarity sit on the edge; this word bears no tail"))
        if (w.unent or w.discharge) and w.grade is None:
            f.append(Finding("E-UNGRADED", "ill-formed", where, "UNENT and discharge need a grade"))
        if w.unent and w.grade not in ("lan", "kas"):
            f.append(Finding("E-UNENT", "ill-formed", where, "UNENT marks AUTH or EXEC only (H2)"))
        if w.rscope and not w.polarity:
            f.append(Finding("E-RSCOPE", "ill-formed", where, "recurrence scope needs a polarity (H3)"))
        if w.scope and not w.polarity:
            f.append(Finding("E-SCOPE", "ill-formed", where, "the scope clitic needs a polarity"))
        if w.incidence == "ol":
            for e in edges:
                if k in (e.origin, e.dest) and e.cls != "BIND":
                    origin = ws[e.origin] if e.origin is not None else None
                    if origin is None or origin.grade != "ti":
                        f.append(Finding("E-OFF", "ill-formed", where,
                                         "an OFF node takes no motion edge unless SIM-graded (A §4.3, §5.5)"))
        if w.coord is not None:
            if not w.head:
                f.append(Finding("E-CARRIER", "ill-formed", where,
                                 "the coordinate is carried only by a head-bearing word (A §4.3)"))
            else:
                into = [e for e in edges if e.dest == k and e.kind == "complete"]
                if not into and w.tail == w.head:
                    f.append(Finding("E-ANCHOR", "ill-formed", where,
                                     "carrier and anchor collapse into one word: the coordinate "
                                     "does not compose (A §5.2a)"))
                elif not into:
                    f.append(Finding("D-ANCHOR", "damaged", where,
                                     "the anchor word is missing: the coordinate is intact and unreadable"))
            if any(s is None for s in w.coord.slots()):
                f.append(Finding("D-SLOT", "damaged", where,
                                 "a coordinate slot is absent, not marked unfilled (A §5.2)"))
            if w.coord.pass_ not in (None, GAP) and w.coord.pass_ not in PASS_VALUES:
                f.append(Finding("E-PASS", "ill-formed", where, f"{w.coord.pass_!r} is not a PASS value"))
            if w.coord.phase not in (None, GAP) and w.coord.phase not in PHASE_VALUES:
                f.append(Finding("E-PHASE", "ill-formed", where, f"{w.coord.phase!r} is not a PHASE value"))
    for e in edges:
        if e.kind == "mismatch":
            f.append(Finding("E-AGREE", "ill-formed", f"words {e.origin + 1}-{e.dest + 1}",
                             "edge halves disagree in class"))
        elif e.kind == "broken-tail":
            known = construction(seg.words[e.origin])
            if known:
                f.append(Finding(known[0], "note", f"word {e.origin + 1}", known[1]))
            else:
                f.append(Finding("D-BROKEN", "damaged", f"word {e.origin + 1}",
                                 f"-{EDGE_CLASSES[e.cls][0]} ⌀"))
        elif e.kind == "broken-head":
            f.append(Finding("D-BROKEN", "damaged", f"word {e.dest + 1}",
                             f"⌀ {EDGE_CLASSES[e.cls][1]}-"))
    if not seg.warrants:
        f.append(Finding("D-WARRANT", "damaged", "segment", "no warrant: catalogued as damaged (A §4.5)"))
    for w in seg.warrants:
        if w not in WARRANTS:
            f.append(Finding("E-WARRANT", "ill-formed", "warrant", f"{w!r} is not a warrant"))
    if "[41]" in seg.warrants and channel not in ("Ch-4", "Ch-1"):
        f.append(Finding("E-41", "ill-formed", "warrant",
                         "[41] is attested in Ch-4 formulae and on three Ch-1 objects only"))
    return f


def well_formed(seg: Segment, channel: str = "Ch-1") -> bool:
    return not any(x.severity == "ill-formed" for x in check(seg, channel))


def reversal_edit(seg: Segment, edge_index: int = 0) -> Segment:
    """Move one edge's tail onto the word that carries its head (A §3.5, §5.2a):
    'mechanically cheap, one CV move'. The result never composes."""
    ws = [replace(w) for w in seg.words]
    complete = [e for e in edges_of(seg) if e.kind == "complete"]
    e = complete[edge_index]
    ws[e.origin] = replace(ws[e.origin], tail=None, grade=None, polarity=None, scope=False,
                           unent=False, discharge=None, rscope=None)
    ws[e.dest] = replace(ws[e.dest], tail=e.cls)
    return Segment(ws, list(seg.warrants), list(seg.free))


def stratum_profile(seg: Segment) -> str:
    """A §7's formal profiles as a classifier over one segment: 'I', 'II', or
    'I/II' when nothing in the segment discriminates (short labels usually)."""
    edges = edges_of(seg)
    reduced = any(e.kind == "reduced" for e in edges)
    stacked = len(seg.warrants) > 1
    has_scope = any(w.scope for w in seg.words)
    has_pol = any(w.polarity for w in seg.words)
    if stacked or has_scope:
        return "I"
    if reduced or has_pol:
        return "II"
    return "I/II"


# --- layer 4: the interlinear gloss line (A §6.3) ---------------------------------

_COORD_SLOT = ("LOC", "PASS", "PHASE")


def gloss_word(w: NodeWord, lex) -> str:
    parts = []
    for slot, form in w.morphemes():
        if slot == "head":
            parts.append(_edge_abbr(w.head, "HEAD"))
        elif slot == "tail":
            parts.append(_edge_abbr(w.tail, "TAIL"))
        elif slot == "root":
            u = lex.by_form.get(form)
            parts.append(u.catalog_gloss if u else f"[{form}](unregistered)")
        else:
            parts.append(abbr_q(BY_SLOT[slot][form]))
    return "-".join(parts)


def _edge_abbr(cls: str, half: str) -> str:
    return f"{cls}.{half}" + ("?" if EDGE_CLASSES[cls][3] == "G3" else "")


def gloss_coord(c: Coordinate, lex) -> str:
    out = []
    for name, v in zip(_COORD_SLOT, c.slots()):
        if v is None:
            out.append(f"{name}.⌀")
        elif v == GAP:
            out.append(f"{name}.GAP")
        elif name == "LOC":
            u = lex.by_form.get(v)
            out.append(u.catalog_gloss if u else f"[{v}]")
        elif name == "PASS":
            out.append(abbr_q(PASS_VALUES[v]))
        else:
            out.append(abbr_q(PHASE_VALUES[v]))
    return "=" + "-".join(out)


def gloss_lines(seg: Segment, lex) -> list[tuple[str, str]]:
    """(transliteration, gloss) columns in A's printed order: node words, then the
    coordinate as its own column after the word that carries it, then free units,
    then the warrants."""
    cols = []
    for w in seg.words:
        base = w.translit().split("=")[0]
        cols.append((base, gloss_word(w, lex)))
        if w.coord is not None:
            cols.append(("=" + w.coord.translit(), gloss_coord(w.coord, lex)))
    for u in seg.free:
        unit = lex.by_form.get(u)
        cols.append((u, unit.catalog_gloss if unit else f"[{u}]"))
    for wr in seg.warrants:
        cols.append((wr, "(warrant slot; no value assigned)" if wr == "[41]" else abbr_q(WARRANTS[wr])))
    return cols


# --- layer 3 in use: the double return (A §6.2) -----------------------------------


def readback(seg: Segment) -> list[str]:
    """The three turns. B expands every edge half to its catalog number — the
    material the initial-syllable rule does not protect (A §6.1d)."""
    from . import phonology as ph
    a_turn = ", ".join(w.translit().split("=")[0].capitalize() for w in seg.words) + "."
    coords = [w.coord for w in seg.words if w.coord is not None]
    if coords:
        a_turn += " " + "-".join(s.capitalize() if i == 0 else s
                                 for i, s in enumerate(coords[0].slots() if coords[0] else [])) + "."
    if seg.warrants:
        a_turn += " " + " ".join(seg.warrants).capitalize() + "."
    b = []
    edge_words = []
    for w in seg.words:
        bits = [w.root.capitalize()]
        if w.incidence:
            bits.append(ph.READBACK_WORDS[INCIDENCE[w.incidence].abbr])
        if w.tail:
            bits.append(ph.edge_word(w.tail))
            edge_words.append(ph.edge_word(w.tail))
        for slot in ("grade", "polarity"):
            v = getattr(w, slot)
            if v:
                bits.append(ph.READBACK_WORDS[BY_SLOT[slot][v].abbr])
        b.append(", ".join(bits) + ".")
    for c in coords:
        names = ("LOC", "PASS", "PHASE")
        words = []
        for n, v in zip(names, c.slots()):
            if v == GAP:
                key = f"{n}.GAP" if n != "LOC" else "LOC.GAP"
            elif n == "PASS":
                key = PASS_VALUES[v].abbr
            elif n == "PHASE":
                key = PHASE_VALUES[v].abbr
            else:
                words.append(f"locus {v}")
                continue
            words.append(ph.READBACK_WORDS[key])
        b.append(", ".join(words).capitalize() + ".")
    if seg.warrants:
        b.append(", ".join(ph.READBACK_WORDS[WARRANTS[x].abbr] for x in seg.warrants).capitalize() + ".")
    confirm = "Confirmed" + ("".join(f", {e}" for e in edge_words)) + "."
    return [a_turn, " ".join(b), confirm]
