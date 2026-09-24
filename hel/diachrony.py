"""The diachronic layer (Phase 1 Q2 as amended; Phase 2 plan item 3b).

Authority C. Tolkien's construction standard, relocated to where canon permits it:
**every sound change here happens in a human mouth or on a committee's table.** The
substrate has no reconstructed phonology and gets none (handoff §5.3; A §6.1). What
has a history is HEL's handling of it, and that history is regular.

Two diachronies, each with ordered laws, relative chronology, and irregulars that are
explained rather than left as noise:

**D1 — the code.** The 1908 Transcription Standard assigned code words on acoustic
criteria, leaked English and Latin mnemonics into six categories (A §6.1e), and let
the core drift into open syllables (A §6.1c). The Reformed List of 1988 replaced it
by five ordered laws. **Engine finding F-08:** the closed forty-eight-syllable list of
A §6.1b cannot be the 1908 list — the retired 1908 strings are not buildable from it —
so it is the Reformed List's, and the 1908 code was an open inventory.

**D2 — the recitation.** The Ch-4 formulae are recited in two branch traditions that
have transmitted them separately for an undetermined period. Their differences are
regular. HEL's comparativists reconstruct a *Common Recitation from the Chicago
notebooks and the Second branch; the reconstruction bottoms out in a human mouth
and cannot be pushed further (P-CH4). This is the comparative engine Phase 1 §4.3
declined as unavailable to a one-system design — recovered on the human side, where
it costs nothing canon protects.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from . import phonology as ph

CLOSED = set(ph.CLOSED)
OPEN = set(ph.OPEN)
ONSET0 = set(ph.ONSETLESS)
LISTED = CLOSED | OPEN | ONSET0
VOWEL_ORDER = "aeiou"

# =================================================================================
# D1 — the 1908 code and the Reformed List of 1988
# =================================================================================

#: 1908 forms of the core roots and ritual units, from the Archive's deprecated
#: register (syllables), with the *heel* the 1988 re-collation recorded on the unit's
#: first notch cluster (the coda the reform supplied), and an irregular class where
#: the laws do not apply. Retired mnemonic strings (A §6.1e) are not reproduced.
CODE_1908 = {
    # form_1988: (syllables_1908, heel, irregular)
    "harnuli": (["ha", "nu", "li"], "r", None),
    "kalsira": (["ka", "si", "ra"], "l", None),
    "telnuro": (["te", "nu", "ro"], "l", None),
    "sarkile": (["sa", "ki"], "r", "R5-recount"),
    "lartuki": (["la", "tu", "ki"], "r", None),
    "kurhali": (["ku", "ha", "li"], "r", None),
    "lunkani": (["lu", "ka", "ni"], "n", None),
    "rukalti": (["ru", "ka", "te"], "l", None),
    "lankiro": (["la", "ki", "ro"], "n", None),
    "siltoni": (["si", "to", "ne"], "l", None),
    "hekasni": (["ke", "ka", "ni"], "s", "R3-scribal"),
    "hasilnu": (["ha", "si", "nu"], "l", None),
    "likasru": (["li", "ka", "ru"], "s", None),
    "kentuli": (["ke", "tu", "li"], "n", None),
    "kanirlu": (["ka", "ni", "lu"], "r", None),
    "tisenlu": (["ti", "se", "lu"], "n", None),
    "ketirnu": (["ke", "ti", "nu"], "r", None),
    "lutirka": (["lu", "ti", "ka"], "r", None),
    "pelhanu": (["pe", "ha", "nu"], "l", None),
    "arhesi": (["a", "he", "si"], "r", None),
    "senlihe": (["se", "li", "he"], "n", None),
    "petirsa": (["pe", "ti", "sa"], "r", None),
    "rasilke": (["ra", "si", "ke"], "l", None),
    "inpelu": (["i", "pe", "lu"], "n", None),
    "nirtoka": (["ni", "to", "ka"], "r", None),
    "tuharli": (["tu", "ha", "li"], "r", None),
    "istuha": (["i", "tu", "ha"], "s", None),
    "sihoslu": (["si", "ho", "lu"], "s", None),
    "olsihe": (["o", "si", "he"], "l", None),
    "munhilu": (["ma", "hi", "lu"], None, None),
    "lunpeki": (["lum", "pe", "ki"], None, None),
    "tulkahe": (["tu", "ka", "he"], "l", None),
    "yuhosli": (["yu", "ho", "li"], "s", None),
    "lusnuhe": (["lu", "nu", "he"], "s", None),
    "kasluhi": (["ka", "lu", "hi"], "s", None),
    "yuntiha": (["yu", "ti", "ha"], "n", None),
    "tokalhi": (["to", "ka", "hi"], "l", None),
    "nukenra": (["nu", "ke", "ra"], "n", None),
    "hitulke": (["hi", "tu", "ke"], "l", None),
    "puhosle": (["pu", "ho", "le"], "s", None),
    "walsenti": (["we", "sen", "ti"], None, None),
    "keharsi": (["ke", "ha", "si"], "r", None),
    "isnuke": (["i", "nu", "ke"], "s", None),
    "arlutu": (["a", "lu", "tu"], "r", None),
    "nisarlu": (["ni", "sar", "lu"], None, None),
    "rosilpe": (["ro", "si", "pe"], "l", None),
    "tuwalsi": (["tu", "wa", "si"], None, None),
    # coordinate fillers: two syllables, exempt from L5, closed by analogy (R4)
    "kihar": (["ki", "ha"], "r", "R4-analogy"),
    "pukal": (["pu", "ka"], "l", "R4-analogy"),
    "rolun": (["ro", "lu"], "n", "R4-analogy"),
    "nikur": (["ni", "ku"], "r", "R4-analogy"),
    "hilun": (None, None, "R2-collision"),     # 1908 gap marker: an English pronoun; see below
}

IRREGULAR = {
    "R1-mnemonic": ("borrowing", "Six categories the 1908 analysts used daily carried English or Latin "
                    "mnemonics (A §6.1e): the reversal-blocked class, the displaced-arrival class, the "
                    "execution grade, the repetition warrant, the ahead value, and the later-pass value. "
                    "Replaced wholesale in 1988 over the 1949 objection. Held in the deprecated register; "
                    "not reproduced."),
    "R2-collision": ("channel", "Respelled because the regular output would have collided with another "
                     "commanded unit on a bad line. The 1908 gap marker would have become wal, which is UNW."),
    "R3-scribal": ("scribal error", "The 1908 form was a branch copyist's /h/–/k/ confusion (the pair the "
                   "code cannot tell apart, A §6.1b), consolidated in 1908 and corrected against the object "
                   "in 1988. The laws would have given ke-."),
    "R4-analogy": ("analogy", "Two-syllable fillers are exempt from the coda rule; the 1988 committee "
                   "closed them anyway so the coordinate paradigm would have one shape (A §6.1c: 'the "
                   "coordinate fillers moved the same way')."),
    "R5-recount": ("re-collation", "The 1988 re-collation found a third notch cluster the 1908 committee "
                   "had read as wear; the unit gained a syllable. The Second branch recites three."),
}


def _nearest_vowel(onset: str, vowel: str, coda: str) -> str | None:
    cands = [v for v in VOWEL_ORDER if (onset + v + coda) in LISTED]
    if not cands:
        return None
    i = VOWEL_ORDER.index(vowel)
    return min(cands, key=lambda v: (abs(VOWEL_ORDER.index(v) - i), VOWEL_ORDER.index(v)))


@dataclass
class Derivation:
    form_1908: str
    heel: str | None
    steps: list = field(default_factory=list)
    result: str = ""
    irregular: str | None = None


def split(s: str):
    on = s[0] if s and s[0] in ph.CONSONANTS else ""
    rest = s[len(on):]
    v = rest[0]
    cd = rest[1:]
    return on, v, cd


def reform_1988(syls: list[str], heel: str | None) -> Derivation:
    """Apply the Reformed List's laws, in order, recording each step."""
    d = Derivation("-".join(syls), heel)
    s = list(syls)

    def log(law, before):
        after = "-".join(s)
        if after != before:
            d.steps.append((law, before, after))

    # L1 — nasal-coda merger: coda m becomes n
    b = "-".join(s)
    s = [x[:-1] + "n" if x.endswith("m") and len(x) > 1 and x[-2] in VOWEL_ORDER else x for x in s]
    log("L1 nasal-coda merger (m > n)", b)
    # L2 — m and w only in closed syllables: open mV, wV take a coda (n after m, l after w)
    b = "-".join(s)
    s = [(x + ("n" if x[0] == "m" else "l")) if x[0] in "mw" and x[-1] in VOWEL_ORDER else x for x in s]
    log("L2 glide and nasal closing", b)
    # L3 — an onsetless open syllable closes with the heel (hiatus is a boundary cue)
    b = "-".join(s)
    if s and s[0] in tuple(VOWEL_ORDER) and heel:
        s[0] = s[0] + heel
        heel = None if s[0] in ONSET0 else heel
    log("L3 onsetless closing", b)
    # L5 — minimum coda rate: 3+ syllables with no coda take the heel on the first
    # syllable that can bear it on the list
    b = "-".join(s)
    has_coda = any(split(x)[2] for x in s)
    if len(s) >= 3 and not has_coda and heel:
        for i, x in enumerate(s):
            if x + heel in CLOSED:
                s[i] = x + heel
                break
        else:
            on, v, _ = split(s[0])
            nv = _nearest_vowel(on, v, heel)
            if nv:
                s[0] = on + nv + heel
    log("L5 minimum coda rate", b)
    # L4 — band accommodation: an unlisted syllable moves its vowel to the nearest in band
    b = "-".join(s)
    out = []
    for x in s:
        if x in LISTED:
            out.append(x)
            continue
        on, v, cd = split(x)
        nv = _nearest_vowel(on, v, cd)
        out.append(on + nv + cd if nv else x)
    s = out
    log("L4 band accommodation", b)
    d.result = "".join(s)
    return d


def d1_table() -> list[dict]:
    rows = []
    for form, (syls, heel, irr) in CODE_1908.items():
        if syls is None:
            rows.append({"form_1988": form, "form_1908": "[deprecated register]", "heel": None,
                         "steps": [], "derived": None, "regular": False, "irregular": irr})
            continue
        d = reform_1988(syls, heel)
        rows.append({"form_1988": form, "form_1908": d.form_1908, "heel": heel, "steps": d.steps,
                     "derived": d.result, "regular": d.result == form and irr is None, "irregular": irr})
    return rows


def d1_check() -> list[str]:
    """Every 1988 form derives regularly, or is an irregular with a stated cause."""
    problems = []
    for r in d1_table():
        if r["irregular"]:
            if r["irregular"] not in IRREGULAR:
                problems.append(f"{r['form_1988']}: unexplained irregular class {r['irregular']}")
            continue
        if r["derived"] != r["form_1988"]:
            problems.append(f"{r['form_1988']}: laws give {r['derived']} from {r['form_1908']}")
    return problems


def coda_count_1908() -> tuple[int, int]:
    """Core roots and ritual units carrying a coda anywhere, 1908 vs 1988 (A §6.1c)."""
    n08 = n88 = total = 0
    for form, (syls, heel, irr) in CODE_1908.items():
        if syls is None or irr == "R4-analogy":
            continue
        total += 1
        n08 += any(split(x)[2] for x in syls)
        n88 += any(ph.is_closed(x) or x in ONSET0 for x in ph.syllables(form))
    return n08, n88, total


# =================================================================================
# D2 — the recitation: the Common Recitation and its two branches
# =================================================================================

#: *Common Recitation, as HEL's comparativists reconstruct it (starred), in a broad
#: phonetic notation with the stress on the first syllable of every word.
#:
#: **Design constraint, stated because it governed every form here.** The recitation is
#: a human tradition inside a Chicago-based institution, so its reconstructed phonology
#: must be *affirmatively* incompatible with Algonquian, Anishinaabe, Potawatomi and
#: Miami-Illinois phonology (prohibited shortcuts #14 and #15; A §6.1a), not merely
#: different. Two earlier drafts of this layer were withdrawn on exactly that test. The
#: first gave the Common Recitation voiced stops, and its daughters grew -nd-, -mb- and
#: -ng-: the clusters A §6.1a names as characteristic of those languages. The second
#: lost intervocalic /h/ in the Second branch, which produced a doubled vowel that reads
#: as Ojibwe double-vowel spelling of length, and word-final -kai, which reads as
#: Polynesian. What stands: the Common Recitation has /f/ — a labiodental, absent from
#: every Algonquian language, and precisely the kind of sound A §6.1 says the 1908
#: committee excluded — and no tautosyllabic cluster, no vowel length, no
#: postalveolar, /r/ throughout.
COMMON = {
    # roots
    "sarkile": "sarkile", "lartuki": "lartuki", "lunkani": "lunkani", "harnuli": "harnuli",
    "yuntiha": "yuntiha", "nisarlu": "nisarlu", "tulkahe": "tulkahe", "lankiro": "lankiro",
    "rosilpe": "rosilfe", "nirtoka": "nirtoka", "olsihe": "olsihe", "tuwalsi": "tuwalsi",
    "inpelu": "infelu", "hasilnu": "hasilnu", "lunpeki": "lunpeki", "telnuro": "telnuro",
    "siltoni": "siltoni", "kanirlu": "kanirlu",
    # formatives
    "in": "in", "is": "is", "ol": "ol", "sil": "sil", "si": "si", "ru": "ru", "halu": "halu",
    "ha": "ha", "pel": "fel", "pe": "fe", "tul": "tul", "tu": "tu", "ken": "ken", "ke": "ke",
    "sen": "sen", "nir": "nir", "kur": "kur", "lan": "lan", "lun": "lun",
    # coordinate fillers
    "hilun": "hilun", "sa": "sa", "to": "to", "nu": "nu", "kihar": "kihar", "nikur": "nikur",
}

V = VOWEL_ORDER


def _palatal(s):
    """S2: k becomes h before i."""
    return s.replace("ki", "hi")


def _raise(s, stressed=True):
    """S3: unstressed e > i and o > u. Stress is word-initial, so a stressed word keeps
    its first vowel; bound formatives are unstressed throughout (A §6.2)."""
    vs = [i for i, c in enumerate(s) if c in V]
    out = list(s)
    for i in (vs[1:] if stressed else vs):
        out[i] = {"e": "i", "o": "u"}.get(out[i], out[i])
    return "".join(out)


def _print(s):
    """C1: the Standard's inventory has no labiodentals (A §6.1); crews who learned the
    formulae from print since 1908 say what is printed."""
    return s.replace("f", "p")


def _chicago_diphthongs(s):
    return s.replace("e", "eɪ").replace("o", "oʊ")


SECOND_LAWS = [
    ("S1 initial stress retained (never adopted the Standard's final stress)", lambda s: s),
    ("S2 k > h before i", _palatal),
    ("S3 unstressed e > i, o > u (after S2: *ke gives ki, never hi)", _raise),
]
SECOND_LAWS_BOUND = [
    ("S1 initial stress retained", lambda s: s),
    ("S2 k > h before i", _palatal),
    ("S3 unstressed e > i, o > u; a bound formative is unstressed throughout", lambda s: _raise(s, False)),
]
ROOTLIKE = {"sarkile", "lartuki", "lunkani", "harnuli", "yuntiha", "nisarlu", "tulkahe", "lankiro",
            "rosilpe", "nirtoka", "olsihe", "tuwalsi", "inpelu", "hasilnu", "lunpeki", "telnuro",
            "siltoni", "kanirlu", "hilun", "sa", "to", "nu", "kihar", "nikur"}
CHICAGO_LAWS = [
    ("C1 labiodentals replaced from print, 1908: f > p, v > w", _print),
    ("C2 final stress from the Standard, 1908", lambda s: s),
    ("C3 Reading Room diphthongs, all positions; no reduction, ever", _chicago_diphthongs),
]


#: Irregulars in the Second branch, each with its cause — the D2 counterpart of D1's
#: R-classes. Engine finding F-27: the collision screen caught the regular output.
SECOND_IRREGULAR = {
    "sen": ("sen", "S-avoid avoidance",
            "S3 predicts sin for the closure marker. The Second branch says sen, and Pellingham (1953) "
            "filed it as the branch's one exception: its crews spoke English, heard 'forbidden' in sin, "
            "and did not say it. The Archive's residue on -sen — English 'forbidden' would supply a "
            "forbidder, and the record names none — is the same objection, made by a committee instead "
            "of a canteen."),
}


def derive(common: str, laws) -> tuple[str, list]:
    s, steps = common, []
    for name, f in laws:
        t = f(s)
        if t != s:
            steps.append((name, s, t))
        s = t
    return s, steps


def d2_table() -> list[dict]:
    rows = []
    for code, cr in COMMON.items():
        sec, s_steps = derive(cr, SECOND_LAWS if code in ROOTLIKE else SECOND_LAWS_BOUND)
        if code in SECOND_IRREGULAR:
            irr, cls, _ = SECOND_IRREGULAR[code]
            s_steps.append((cls, sec, irr))
            sec = irr
        chi, c_steps = derive(cr, CHICAGO_LAWS)
        rows.append({"code_1988": code, "common": "*" + cr, "second": sec, "chicago": chi,
                     "second_steps": s_steps, "chicago_steps": c_steps,
                     "code_is_printed_chicago": _print(cr) == code})
    return rows


def d2_check() -> list[str]:
    """The 1988 code form of every recited unit is the Common Recitation as printed."""
    return [f"{r['code_1988']}: {r['common']} does not print as the code form"
            for r in d2_table() if not r["code_is_printed_chicago"]]


def algonquian_check(forms) -> list[str]:
    """Every reconstructed or branch form stays outside the four features A §6.1a names:
    no vowel length, no tautosyllabic cluster (esp. -shk- -nd- -mb- -ng-), /r/ allowed,
    no /tʃ/ /ʃ/."""
    bad = []
    for f in forms:
        for x in ("shk", "sk", "nd", "mb", "ng", "nk", "mp", "nt", "sh", "ch", "aa", "ii", "oo", "uu", "ee"):
            if x in f.replace("ˈ", ""):
                if x in ("nk", "mp", "nt") and _heterosyllabic(f, x):
                    continue
                bad.append(f"{f}: contains {x}")
    return bad


def _heterosyllabic(f, x):
    # a coda nasal before an onset stop across a syllable boundary (lun.ka.ni) is the
    # Standard's own shape and not a cluster; only word-final or pre-consonantal counts
    i = f.find(x)
    return i >= 0 and i + 2 < len(f) and f[i + 2] in V


#: The Archive's reconstruction, and who accepts which law. At least one law is
#: accepted by only two of the three schools (Phase 1 §5 item 3b).
RECONSTRUCTION = [
    {"law": "Common *f (Chicago p : Second f)", "grade": "G3", "analyst": "Pellingham 1953",
     "Utterance": True, "Palimpsest": True, "Instrument": False,
     "dispute": "Four recited units have Chicago p against Second f; one (lunpeki) has p in both. The "
                "comparativists reconstruct two sounds, *p and *f, and read Chicago's p as print: the "
                "Standard has no labiodental, and crews who learned from it say what is printed. The "
                "Instrument school reads the Second branch's f as its own lenition of p and lunpeki as a "
                "post-1908 loan from Chicago into the one formula the Second branch adopted late. Both "
                "accounts fit every form. Unresolved, and the f is a shibboleth either way."},
    {"law": "k > h before i, older than the raising", "grade": "G2", "analyst": "Tredgold 1967",
     "Utterance": True, "Palimpsest": True, "Instrument": True,
     "dispute": "Relative chronology from one form: the THRU tail *ken is kin in the Second branch, not "
                "hin. Had the raising come first, e > i would have fed the palatal law."},
    {"law": "Initial stress in the Common Recitation", "grade": "G2", "analyst": "the notebooks",
     "Utterance": True, "Palimpsest": True, "Instrument": True,
     "dispute": "The Chicago notebooks mark it; the Standard's final stress is minuted as a 1908 choice."},
    {"law": "Second-branch raising of unstressed e and o", "grade": "G2", "analyst": "Tredgold 1967",
     "Utterance": True, "Palimpsest": True, "Instrument": True,
     "dispute": "Why the Standard's performance rule says 'no reduction, ever': it was written against a "
                "branch that already had."},
    {"law": "H4: the Second branch has lost its head halves", "grade": "G2", "analyst": "Treloar 1926",
     "Utterance": True, "Palimpsest": True, "Instrument": True,
     "dispute": "Head halves are spoken unstressed and fast; a tradition that never learned from print "
                "kept only the tails. The attrition rule (Phase 1 H4), observed in the branch that tests it."},
    {"law": "Heel codas = recitation codas", "grade": "G3", "analyst": "the 1988 committee",
     "Utterance": True, "Palimpsest": False, "Instrument": True,
     "dispute": "The 1988 heels agree with the recitations' codas unit for unit. Two lines of evidence, or "
                "one: the Palimpsest school notes that the re-collators knew the recitations and found the "
                "heels they expected (the objection A-reserve §4.1 prints about unit boundaries)."},
]


#: The formulae in both branches (IPA, broad), built from the laws above. H4 applies
#: in the Second branch only: head halves are unstressed and fast, and the branch that
#: never learned from print has lost them.
def recite(formula_text: str, branch: str) -> str:
    """A formula as each branch recites it (broad IPA). H4 applies in the Second branch
    only: head halves are unstressed and fast, and the branch that never learned the
    formulae from print has lost them."""
    words = []
    for chunk in formula_text.split("·"):
        chunk = chunk.strip()
        if chunk == "[41]":
            words.append("ˈfɔɹti ˈwʌn")
            continue
        base, _, coord = chunk.partition("=")
        ms = base.split("-")
        if branch == "second" and len(ms) > 1 and ms[0] in ("si", "ru", "ha", "pe", "tu", "ke"):
            ms = ms[1:]
        def lw(m, first):
            if branch != "second":
                return CHICAGO_LAWS
            return SECOND_LAWS if (first and m in ROOTLIKE) or m in ("hilun", "sa", "to", "nu", "kihar", "nikur") \
                else SECOND_LAWS_BOUND
        forms = [SECOND_IRREGULAR[m][0] if branch == "second" and m in SECOND_IRREGULAR
                 else derive(COMMON.get(m, m), lw(m, i == 0))[0] for i, m in enumerate(ms)]
        cforms = [derive(COMMON.get(m, m), lw(m, True))[0] for m in coord.split("-")] if coord else []
        w = "-".join(forms) + ("=" + "-".join(cforms) if cforms else "")
        if branch == "second":
            w = "ˈ" + w
        words.append(w)
    return " · ".join(words)
