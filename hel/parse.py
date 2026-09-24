"""Transliteration → structure, and the Stratum III classifier.

Authority C. The parser reads layer 2 exactly as the Archive prints it: node words
joined by the editorial hyphen (A §4: HEL's, not the source's), the coordinate
after ``=``, segments' parts separated by `` · ``, stacked warrants by spaces.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from . import grammar as g
from . import phonology as ph
from .lexicon import Lexicon, default as default_lexicon

SUFFIX_SLOTS = {
    "incidence": g.INCIDENCE, "tail": g.TAILS, "grade": g.GRADES, "unent": g.UNENT,
    "discharge": g.DISCHARGE, "polarity": g.POLARITY, "rscope": g.RSCOPE, "scope": g.SCOPE,
}
_SUFFIX_FORMS = {}
for _slot, _table in SUFFIX_SLOTS.items():
    for _form in _table:
        assert _form not in _SUFFIX_FORMS, f"suffix form {_form} is ambiguous across slots"
        _SUFFIX_FORMS[_form] = _slot
_ORDER = {s: i for i, s in enumerate(g.SUFFIX_ORDER)}


class ParseError(ValueError):
    pass


def parse_word(text: str, lex: Optional[Lexicon] = None) -> g.NodeWord:
    lex = lex or default_lexicon()
    word, _, coord = text.partition("=")
    ms = word.split("-")
    if not all(ms):
        raise ParseError(f"empty morpheme in {text!r}")
    head = None
    if len(ms) > 1 and ms[0] in g.HEADS and ms[1] not in _SUFFIX_FORMS:
        head = g.HEADS[ms[0]].cls
        ms = ms[1:]
    root, rest = ms[0], ms[1:]
    if not ph.is_transliteration(root):
        raise ParseError(f"{root!r} is not a transliteration (off the 1908 list)")
    nw = g.NodeWord(root=root, head=head)
    last = -1
    for m in rest:
        slot = _SUFFIX_FORMS.get(m)
        if slot is None:
            raise ParseError(f"{m!r} in {text!r} is not a suffix formative")
        if _ORDER[slot] <= last:
            raise ParseError(f"{m!r} ({slot}) out of template order in {text!r}")
        last = _ORDER[slot]
        if slot == "tail":
            nw.tail = g.TAILS[m].cls
        elif slot == "unent":
            nw.unent = True
        elif slot == "scope":
            nw.scope = True
        else:
            setattr(nw, slot, m)
    if coord or text.endswith("="):
        parts = coord.split("-") if coord else []
        slots = (parts + [None, None, None])[:3]
        slots = [s if s else None for s in slots]
        nw.coord = g.Coordinate(*slots)
    return nw


def parse_segment(text: str, lex: Optional[Lexicon] = None) -> g.Segment:
    lex = lex or default_lexicon()
    chunks = [c.strip() for c in text.split("·")]
    words, free, warrants = [], [], []
    for c in chunks:
        toks = c.split()
        if all(t in g.WARRANTS for t in toks):
            warrants += toks
        elif len(toks) == 1 and lex.is_ritual(toks[0]):
            free.append(toks[0])
        elif len(toks) == 1:
            words.append(parse_word(toks[0], lex))
        else:
            raise ParseError(f"cannot read chunk {c!r}")
    return g.Segment(words, warrants, free)


# --- the Stratum III classifier (A-reserve §2) ----------------------------------------


def assignable(unit: str, lex: Lexicon) -> Optional[str]:
    """Condition 1's table lookup, positional. Returns the reading that assigns the
    unit to a functional paradigm, or None.

    A unit is assignable if it *is* a formative, a coordinate filler, a warrant or a
    registered functional root; or if it segments as a well-formed node word
    (optional head, registered root, suffixes in template order).

    **Engine finding F-05.** The reserve (§8.2) defeats the 1971 extraction of ``ar``
    from ``pekalar`` because "an incidence marker is by definition what stands between
    a root and an edge tail". A's own label objects contradict that wording: they
    carry ``-ar`` on a word with no edge half at all (A §4.6b). The criterion that
    does the reserve's work without the contradiction is the one implemented here —
    an incidence marker must be incident to a *registered root*. ``pekal`` is not in
    the register, so ``ar`` has no address; and the 1971 author's rejoinder, that a
    paradigm which can only find itself where it already is has not been tested, is
    now exactly true of the test.
    """
    if unit in _SUFFIX_FORMS or unit in g.HEADS:
        return f"formative {unit}"
    if unit in g.WARRANTS or unit in g.PASS_VALUES or unit in g.PHASE_VALUES or unit == g.GAP:
        return f"free formative {unit}"
    if lex.is_registered_root(unit):
        return f"registered root {unit}"
    for seg in ph.segment(unit):
        # try every split of the syllable string into morphemes
        for reading in _node_word_readings(seg, lex):
            return reading
    return None


def _node_word_readings(sylls, lex: Lexicon):
    n = len(sylls)
    for h in (0, 1):
        if h and sylls[0] not in g.HEADS:
            continue
        for r_end in range(h + 1, n + 1):
            root = "".join(sylls[h:r_end])
            if not lex.is_registered_root(root):
                continue
            rest = sylls[r_end:]
            if _suffixes_ok(rest):
                return [f"node word {'-'.join(([sylls[0]] if h else []) + [root] + list(rest))}"]
    return []


def _suffixes_ok(sylls) -> bool:
    # suffix formatives are one syllable except the RECUR tail -halu (two)
    i, last = 0, -1
    while i < len(sylls):
        two = "".join(sylls[i:i + 2])
        if two in _SUFFIX_FORMS and len(two) > len(sylls[i]):
            m, i = two, i + 2
        else:
            m, i = sylls[i], i + 1
        slot = _SUFFIX_FORMS.get(m)
        if slot is None or _ORDER[slot] <= last:
            return False
        last = _ORDER[slot]
    return True


@dataclass
class FieldReport:
    """What the conservator and the object record supply for Condition 2."""
    intact: bool = True
    contact: bool = False
    channel: str = "Ch-1"
    photographic: bool = True        # Ch-2: original plate, not a copyist's hand
    branch_traditions: int = 0       # Ch-4: independent traditions attesting it


@dataclass
class Classification:
    klass: str                       # "III", "III (provisional)", "unassigned, short", "not III"
    reasons: list = field(default_factory=list)
    assigned: dict = field(default_factory=dict)


def classify_iii(units: list[str], report: FieldReport, lex: Optional[Lexicon] = None) -> Classification:
    lex = lex or default_lexicon()
    reasons, assigned = [], {}
    for u in units:
        a = assignable(u, lex)
        if a:
            assigned[u] = a
    if assigned:
        reasons.append(f"Condition 1 fails: {len(assigned)} assignable unit(s)")
    if not report.intact:
        reasons.append("Condition 2(a) fails: field not certified intact")
    if report.contact:
        reasons.append("Condition 2(b) fails: contact with functional material")
    if report.channel == "Ch-2" and not report.photographic:
        reasons.append("Condition 2(c) fails: Ch-2 copy is a copyist's hand, not a plate")
    if report.channel == "Ch-4" and report.branch_traditions < 2:
        reasons.append("Condition 2(c) fails: Ch-4 needs two independent branch traditions")
    if report.channel == "Ch-3":
        reasons.append("no Stratum III material has ever been catalogued from Ch-3")
    if reasons:
        return Classification("not III", reasons, assigned)
    if len(units) < 6:
        return Classification("unassigned, short", ["Condition 3: fewer than six units"], assigned)
    if len(units) < 9:
        return Classification("III (provisional)", ["six to eight units"], assigned)
    return Classification("III", [], assigned)
