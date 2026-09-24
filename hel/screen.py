"""The collision screen (Phase 1 §4.5 standing rule; the gate left open at Phase 1).

Authority C. **A screening aid, not a guarantee.** The certification this module
supports is a statement of what was done — these forms, these families, this date,
these residuals, this rejects list — never a claim of purity (Phase 1 §4.5).

Method, stated so it can be argued with:

1. **Exact** — the form, or any syllable-aligned substring of three letters or more,
   is a listed entry.
2. **Contained** — a listed entry of four letters or more occurs anywhere in the form
   (the ``pelunar``/*lunar* and ``walniken``/*Nike* case).
3. **Sounds-like** — both strings are folded into the 1908 inventory (voicing
   neutralised, fricatives to their nearest listed consonant, digraphs collapsed) and
   compared; an edit distance of 1 against an entry of five letters or more, or 0
   against a shorter one, is a hit.

Severity is weighted by category (obscene/slur/indigenous highest) and by position
(free units are screened harder than bound ones — A §6.1f's stated weighting).
Wordlists live in ``data/screen/*.txt`` as ``entry<TAB>category<TAB>gloss``.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from . import phonology as ph

SCREEN_DIR = Path(__file__).resolve().parent.parent / "data" / "screen"

SEVERITY = {
    "obscene": 5, "slur": 5, "indigenous": 5, "ethnonym": 5, "vulgar": 4, "bodily": 3,
    "deity": 4, "religious": 3, "brand": 3, "person": 2, "site": 3, "place": 2,
    "fiction": 3, "astro": 3, "latin": 2, "comic": 3, "loaded": 3, "common": 2,
}
#: Hits at or above this severity reject a free unit; bound formatives need +1.
REJECT_AT = 3

_FOLD = [
    ("sch", "s"), ("sh", "s"), ("ch", "t"), ("th", "t"), ("ph", "p"), ("gh", "k"),
    ("ck", "k"), ("qu", "kw"), ("ng", "n"), ("ll", "l"),
]
_MAP = str.maketrans({
    "b": "p", "d": "t", "g": "k", "v": "w", "f": "p", "z": "s", "c": "k", "q": "k",
    "x": "ks", "j": "y",
})


def fold(s: str) -> str:
    """Fold any romanized string into the 1908 inventory's sound space."""
    s = s.lower()
    s = re.sub(r"[^a-z]", "", s)
    for a, b in _FOLD:
        s = s.replace(a, b)
    s = s.translate(_MAP)
    s = re.sub(r"(.)\1+", r"\1", s)   # no geminates in the code, so none in the fold
    return s


@dataclass(frozen=True)
class Entry:
    text: str
    folded: str
    category: str
    gloss: str
    family: str


@lru_cache(maxsize=1)
def wordlists() -> tuple[Entry, ...]:
    out = []
    if not SCREEN_DIR.exists():
        return ()
    for p in sorted(SCREEN_DIR.glob("*.txt")):
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.split("\t")
            text = parts[0].strip().lower()
            cat = parts[1].strip() if len(parts) > 1 else "loaded"
            gloss = parts[2].strip() if len(parts) > 2 else ""
            if len(text) >= 2:
                out.append(Entry(text, fold(text), cat, gloss, p.stem))
    return tuple(out)


@dataclass
class Hit:
    form: str
    entry: Entry
    how: str
    severity: int


def _edit1(a: str, b: str) -> bool:
    if abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) <= 1
    if len(a) > len(b):
        a, b = b, a
    i = j = diff = 0
    while i < len(a) and j < len(b):
        if a[i] != b[j]:
            diff += 1
            j += 1
            if diff > 1:
                return False
        else:
            i += 1; j += 1
    return True


#: The structural screen for real Indigenous-language material (A-reserve §10;
#: prohibited shortcut #14), run affirmatively on every form by the method the reserve
#: states: the profile must be *actively incompatible* with Algonquian, Anishinaabe,
#: Potawatomi and Miami-Illinois. **It holds no Indigenous word list and builds none.**
#: A lexical screen against those languages is work for a reviewer with
#: community-sanctioned resources; it is recorded as a gap, not simulated.
#:
#: Engine finding F-26: the closed list can spell ``sh`` across a syllable boundary
#: (an s-coda before an h-onset, ``kas-hi``), and a reader sees a postalveolar in it.
#: No core unit does; 25 forms coined by the first Phase 2 build did, and the screen
#: now rejects the junction in coinage.
STRUCTURAL = [
    (re.compile(r"(aa|ee|ii|oo|uu)"), "a doubled vowel reads as vowel length (double-vowel orthography)"),
    (re.compile(r"sh"), "an s-coda before an h-onset spells sh, which reads as a postalveolar the profile excludes"),
    (re.compile(r"(nd|mb|ng|zh|ch|kw)"), "a cluster the profile excludes"),
]


def structural(form: str, bound: bool = False) -> list[Hit]:
    out = []
    for rx, why in STRUCTURAL:
        m = rx.search(form.lower())
        if m:
            e = Entry(m.group(0), m.group(0), "indigenous", why, "structural")
            out.append(Hit(form, e, "structural", SEVERITY["indigenous"] - (1 if bound else 0)))
    return out


def screen(form: str, bound: bool = False) -> list[Hit]:
    """All hits on one form, most severe first.

    Raw-string matches carry their category's full weight. A match found only after
    folding is a *sounds-like* match and weighs one less: folding models what a
    listener might hear, and a reader sees the letters (``rukalti`` holds *alti*, not
    *Aldi*). Entries under three letters are never matched — every two-letter syllable
    is a word somewhere, and the reserve's method starts at three (A-reserve §10).
    """
    translit = ph.is_transliteration(form)
    hits = structural(form, bound) if translit else []
    f = fold(form)
    syl = ph.syllables(form) if translit else (form,)
    # syllable-aligned substrings of 3+ letters
    subs = set()
    for i in range(len(syl)):
        for j in range(i + 1, len(syl) + 1):
            s = "".join(syl[i:j])
            if len(s) >= 3:
                subs.add(s)
    fsubs = {fold(s) for s in subs}
    for e in wordlists():
        if len(e.text) < 3:
            continue
        how, folded = None, False
        if e.text == form:
            how = "exact"
        elif e.text in subs:
            how = "syllable-substring"
        elif len(e.text) >= 4 and e.text in form:
            how = "contains"
        elif len(e.folded) >= 4:
            folded = True
            if e.folded == f:
                how = "exact (folded)"
            elif e.folded in fsubs:
                how = "syllable-substring (folded)"
            elif e.folded in f:
                how = "contains (folded)"
            elif len(e.folded) >= 5 and _edit1(e.folded, f):
                how = "sounds-like"
        if how:
            sev = SEVERITY.get(e.category, 2) - (1 if folded else 0) - (1 if bound else 0)
            hits.append(Hit(form, e, how, sev))
    return sorted(hits, key=lambda h: -h.severity)


def passes(form: str, bound: bool = False) -> bool:
    return not any(h.severity >= REJECT_AT for h in screen(form, bound))


def report(forms, bound=False) -> dict:
    """Rejected forms and residuals, the shape of a screen statement (A-reserve §10)."""
    out = {"screened": len(forms), "rejected": {}, "residuals": {}}
    for f in forms:
        hs = screen(f, bound)
        if any(h.severity >= REJECT_AT for h in hs):
            out["rejected"][f] = [(h.entry.text, h.entry.category, h.entry.family, h.how) for h in hs[:3]]
        elif hs:
            out["residuals"][f] = [(h.entry.text, h.entry.category, h.entry.family, h.how) for h in hs[:3]]
    return out


def canon_forms() -> dict:
    """Every form the design has fixed, by class, for the screen statement."""
    import yaml
    from . import diachrony, grammar as g
    root = SCREEN_DIR.parent
    core = yaml.safe_load((root / "core.yaml").read_text(encoding="utf-8"))
    units = core.get("units") or core.get("roots") or []
    fe = yaml.safe_load((root / "field_english.yaml").read_text(encoding="utf-8"))
    out = {
        "core and ritual units": sorted({u["form"] for u in units}),
        "bound formatives": sorted({f.form for f in g.FORMATIVES if len(f.form) >= 2}),
        "CSC-1146 and its variant": ["walnisen", "pehisar", "tirakur", "pekalar", "munlisen", "nusar", "nulisar"],
        "Second-branch forms": sorted({r["second"] for r in diachrony.d2_table()}),
        "Field English loans": sorted({l["loan"] for l in fe["loans"] if ph.is_transliteration(l["loan"])}),
        "in-world names": ["Sowerby", "Hessell", "Treloar", "Thaxter", "Merrow", "Pellingham", "Tredgold",
                           "Keele", "Cardwell", "Onslow", "Hallam", "Redfern", "Ashcroft", "Vance", "Aubrey",
                           "Sturge", "Rowntree"],
    }
    return out


def main():
    """The screen statement for every fixed form. A hit at rejection weight on a fixed
    form is not a rejection — the form is in the record — it is a disclosure, and each
    one is adjudicated in docs/08-THE-ENGINE.md."""
    total = 0
    for cls, forms in canon_forms().items():
        bound = cls == "bound formatives"
        rep = report([f.lower() for f in forms], bound=bound)
        total += len(forms)
        print(f"== {cls}: {len(forms)} screened, {len(rep['rejected'])} rejected, {len(rep['residuals'])} residual")
        for f, hs in {**rep["rejected"], **rep["residuals"]}.items():
            tag = "DISCLOSE" if f in rep["rejected"] else "residual"
            print(f"   {tag:8} {f}: " + "; ".join(f"{t} ({c}, {fam}, {how})" for t, c, fam, how in hs))
    print(f"{total} forms; {len(wordlists())} list entries in {len({e.family for e in wordlists()})} lists")


if __name__ == "__main__":
    main()
