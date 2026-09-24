"""Layer 2 and layer 3: the 1908 Transcription Standard as executable rules.

Authority C. Implements A §6.1b-e (the sanctioned list, the minimum coda rate, the
initial-syllable distinctness rule) and A §6.2 (HEL field pronunciation), with one
repair the engine forced — see ``ONSETLESS_POSITIONS``.

Nothing about the sound of any form here is evidence about the source (A §6.1).
The code is HEL's: a radio and telephone code chosen by a committee.
"""
from __future__ import annotations

from collections import defaultdict
from functools import lru_cache

# --- the code book (A §6.1b) -------------------------------------------------

CONSONANTS = tuple("p t k s h m n l r w y".split())
VOWELS = tuple("a e i o u".split())
CODAS = tuple("n s r l".split())

OPEN = tuple("ha he hi ka ke ki le li lu ni nu pe pu ra ro ru sa si ti to tu yu".split())
CLOSED = tuple(("har hos kal kas ken kur lan lar lun lus mun nes nir pel sar sen sil "
                "tel tir tul wal yun").split())
ONSETLESS = tuple("ar in is ol".split())
SANCTIONED = OPEN + CLOSED + ONSETLESS
assert len(SANCTIONED) == 48 and len(set(SANCTIONED)) == 48

#: Where an onsetless syllable may stand. **Repair (engine finding F-01).** A §6.1b
#: licensed the four onsetless syllables "for the incidence markers only". Two other
#: claims in A require them elsewhere: §6.1d's commanded core of forty-eight units
#: with forty-eight distinct first syllables (only 44 listed syllables have an onset),
#: and §7's Stratum II environment, which is defined over *vowel-initial roots*.
#: Both hold only if a root may begin with an onsetless syllable. The repair keeps
#: the committee's own rationale — hiatus is a boundary cue — and extends it to the
#: one other boundary where hiatus arises: between a head half and a root.
ONSETLESS_POSITIONS = ("incidence", "root-initial")

SYLLABLE_SET = frozenset(SANCTIONED)


def onset(syl: str) -> str:
    return syl[0] if syl and syl[0] in CONSONANTS else ""


def nucleus(syl: str) -> str:
    return next(c for c in syl if c in VOWELS)


def coda(syl: str) -> str:
    return syl[-1] if syl[-1] in CODAS and len(syl) > 1 and syl[-2] in VOWELS else ""


def is_closed(syl: str) -> bool:
    return bool(coda(syl))


@lru_cache(maxsize=65536)
def segment(word: str) -> tuple[tuple[str, ...], ...]:
    """Every segmentation of ``word`` into sanctioned syllables (string level).

    The segmentation is purely orthographic: it says which listed syllables spell
    the string. Whether a syllable is *licensed where it stands* is a separate
    question (``licensed``), and the difference is exactly the 1971 lesson of
    A-reserve §8.2: ``pe-kal-ar`` spells ``pekalar`` legally and still fails on
    position.
    """
    if not word:
        return ((),)
    out = []
    for syl in SANCTIONED:
        if word.startswith(syl):
            for rest in segment(word[len(syl):]):
                out.append((syl,) + rest)
    return tuple(out)


def syllables(word: str) -> tuple[str, ...]:
    """The Standard's syllabification: the first segmentation, preferring the
    reading with no medial onsetless syllable (the committee's tie-break)."""
    segs = segment(word)
    if not segs:
        raise ValueError(f"{word!r} is not a transliteration: not built from the 1908 list")
    clean = [s for s in segs if not any(x in ONSETLESS for x in s[1:])]
    return (clean or list(segs))[0]


def is_transliteration(word: str) -> bool:
    return bool(segment(word))


def licensed_as_root(word: str) -> tuple[bool, str]:
    """A root form: built from the list, vowel-final (A §6.1), onsetless only
    root-initially (F-01), and obeying the minimum coda rate (A §6.1c)."""
    segs = [s for s in segment(word) if not any(x in ONSETLESS for x in s[1:])]
    if not segs:
        return False, "not spelled from the list with onsetless syllables only root-initially"
    s = segs[0]
    if coda(s[-1]):
        return False, "roots are vowel-final in the Standard (A §6.1)"
    for a, b in zip(s, s[1:]):
        if coda(a) and onset(b) == coda(a):
            return False, "no geminates (A §6.1): a coda may not repeat the next onset"
    if len(s) >= 3 and not any(is_closed(x) or x in ONSETLESS for x in s):
        return False, "minimum coda rate: 3+ syllables need a coda (A §6.1c, 1988)"
    return True, ""


def meets_coda_rate(word: str) -> bool:
    s = syllables(word)
    return len(s) < 3 or any(is_closed(x) or x in ONSETLESS for x in s)


def first_syllable(word: str) -> str:
    return syllables(word)[0]


def initial_distinctness(units) -> dict:
    """A §6.1d: no two units of the commanded core share their first syllable."""
    seen = defaultdict(list)
    for u in units:
        seen[first_syllable(u)].append(u)
    return {k: v for k, v in seen.items() if len(v) > 1}


def commanded_core_cap() -> int:
    """How many units can have distinct first syllables, given where onsetless
    syllables are licensed. 48 under the F-01 repair; 44 without it."""
    if "root-initial" in ONSETLESS_POSITIONS:
        return len(SANCTIONED)
    return len(OPEN) + len(CLOSED)


def bands() -> dict:
    """Vowel bands per onset, per syllable type. A §6.1b states the open bands;
    the closed bands differ (e.g. /h/ opens only with {a e i} but closes as
    ``har`` and ``hos``), which the prose did not say."""
    out = {"open": defaultdict(set), "closed": defaultdict(set)}
    for s in OPEN:
        out["open"][onset(s)].add(nucleus(s))
    for s in CLOSED:
        out["closed"][onset(s)].add(nucleus(s))
    return {k: {c: "".join(sorted(v)) for c, v in sorted(d.items())} for k, d in out.items()}


def confusion_table() -> dict:
    """A §6.1b's measurement: substitute every other licensed onset into every
    listed syllable and count how many land off the list (detectable)."""
    res = {"open": [0, 0], "closed": [0, 0], "pairs_undetectable": []}
    for s in SANCTIONED:
        on = onset(s)
        if not on:
            continue
        kind = "closed" if is_closed(s) else "open"
        for c in CONSONANTS:
            if c == on:
                continue
            t = c + s[1:]
            res[kind][0] += 1
            if t not in SYLLABLE_SET:
                res[kind][1] += 1
            else:
                res["pairs_undetectable"].append((s, t))
    total = res["open"][0] + res["closed"][0]
    det = res["open"][1] + res["closed"][1]
    res["total"] = total
    res["detectable"] = det
    return res


# --- layer 3: HEL field pronunciation (A §6.2) --------------------------------

_IPA_C = {"p": "p", "t": "t", "k": "k", "s": "s", "h": "h", "m": "m", "n": "n",
          "l": "l", "r": "ɹ", "w": "w", "y": "j"}
_IPA_V = {
    "standard": {"a": "a", "e": "e", "i": "i", "o": "o", "u": "u"},        # 1949 Standard
    "chicago": {"a": "a", "e": "eɪ", "i": "i", "o": "oʊ", "u": "u"},       # Reading Room
}
TRADITIONS = tuple(_IPA_V)


def ipa_syllable(syl: str, tradition: str = "standard") -> str:
    v = _IPA_V[tradition]
    return "".join(_IPA_C[c] if c in _IPA_C else v[c] for c in syl)


def ipa_word(morphemes, stressed_index: int, tradition: str = "standard") -> str:
    """IPA for one spoken word given its morphemes and the index of the morpheme
    whose final syllable takes stress. No reduction, ever (C's documentation
    standard, adopted at Phase 1 §4.3)."""
    parts = []
    for i, m in enumerate(morphemes):
        if m.startswith("["):
            parts.append(["ˈfɔɹti.wʌn"])  # [41]: said as the English numeral
            continue
        syls = [ipa_syllable(s, tradition) for s in syllables(m)]
        if i == stressed_index:
            syls[-1] = "ˈ" + syls[-1]
        parts.append(syls)
    return ".".join(s for p in parts for s in p)


# --- the double return (A §6.2) ----------------------------------------------

#: The Archive's edge-class numbers, used in the readback. Fixed by A §6.2's
#: example (THRU is "edge seven", PASS "edge one"); the others follow the order
#: in which the 1908 consolidation catalogued the classes.
EDGE_NUMBER = {"PASS": 1, "BAR": 2, "SHUNT": 3, "RECUR": 4, "BIND": 5, "ADJ": 6, "THRU": 7}
_NUMBER_WORD = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven"}
READBACK_WORDS = {
    "TERM": "terminal", "MED": "medial", "JCT": "junction", "OFF": "off-path",
    "SIM": "modeled", "PREP": "staged", "AUTH": "grade three", "EXEC": "executed",
    "IMP": "impossible", "FRB": "closed", "UNA": "unavailable", "UNV": "unverified",
    "SCOPE": "edge-scoped",
    "REG": "registered", "WIT": "witnessed", "REP": "recurrent", "INF": "inferred",
    "UNW": "unsourced", "41": "forty-one",
    "LOC.GAP": "locus open", "PASS.SAME": "pass same", "PASS.LATER": "pass later",
    "PASS.OTHER": "pass other", "PASS.GAP": "pass open",
    "PHASE.SAME": "phase at anchor", "PHASE.AHEAD.MEAS": "phase measured ahead",
    "PHASE.BEHIND.MEAS": "phase measured behind", "PHASE.DISP.UNMEAS": "phase displaced",
    "PHASE.GAP": "phase open",
}


def edge_word(cls: str) -> str:
    return f"edge {_NUMBER_WORD[EDGE_NUMBER[cls]]}"
