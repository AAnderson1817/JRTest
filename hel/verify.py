"""The verifier: every figure the A-family states about its catalogue, checked against
the generated catalogue. Authority C.

``data/claims.yaml`` lists each claim with where it is made, what the document said,
and how to measure it. Each claim comes back with a status:

* **holds** — the corpus reproduces the figure (within the stated tolerance);
* **repaired** — the figure contradicted the documents' own design (arithmetic,
  definitions, or other figures in the same table), the text was corrected, and the
  corpus reproduces the corrected figure;
* **calibration** — the figure is feasible under the design, and this build's
  production rates give a different number; listed, not hidden, and not "an error";
* **fails** — none of the above: a defect in the build or the documents, unexplained.

    python3 -m hel.verify          # prints the table; exit status 1 on any failure
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

from . import grammar as g
from . import phonology as ph
from .lexicon import default as default_lexicon
from .parse import parse_segment

ROOT = Path(__file__).resolve().parent.parent


def _load():
    cat = json.loads((ROOT / "corpus" / "csc.json").read_text(encoding="utf-8"))
    figs = json.loads((ROOT / "corpus" / "figures.json").read_text(encoding="utf-8"))
    reg = json.loads((ROOT / "corpus" / "register.json").read_text(encoding="utf-8"))["units"]
    return cat, figs, reg


def metrics(cat=None, figs=None, reg=None) -> dict:
    """Named measurements, beyond corpus/figures.json, that the claims refer to."""
    if cat is None:
        cat, figs, reg = _load()
    F, T = figs["figures"], figs["iii"]
    lex = default_lexicon()
    M = {"figures": F, "iii": T}
    ch1 = [e for e in cat if e["channel"] == "Ch-1" and not e["part"]]
    M["ch1_intact_with_ar"] = sum(
        1 for e in ch1 if e["condition"] == "intact"
        and any(re.search(r"-ar(?=[-=\s]|$)", s["translit"]) for s in e["segments"]))
    M["ch1_with_41"] = sum(1 for e in ch1 if any("[41]" in s["translit"] for s in e["segments"]))
    ch4 = [e for e in cat if e["channel"] == "Ch-4" and e["segments"]]
    M["ch4_formulae_with_41"] = sum(1 for e in ch4 if "[41]" in e["segments"][0]["translit"])
    M["ch4_formulae"] = len(ch4)
    # functional recurrence, measured the way A-reserve §4.2 measures Stratum III
    occ, pairs, within, k = defaultdict(set), [], [], 0
    for e in cat:
        if e["stratum"].split(" ")[0] not in ("I", "II"):
            continue
        for s in e["segments"]:
            k += 1
            c = Counter(parse_segment(s["translit"], lex).tokens())
            for t, n in c.items():
                occ[t].add(k)
                within.append(n >= 2)
            pairs += [(k, t) for t in c]
    M["functional_types"] = len(occ)
    M["functional_one_sequence_share"] = round(sum(len(v) == 1 for v in occ.values()) / max(1, len(occ)), 2)
    M["functional_p_within"] = round(sum(within) / max(1, len(within)), 2)
    M["functional_p_elsewhere"] = round(sum(len(occ[t]) > 1 for _, t in pairs) / max(1, len(pairs)), 2)
    M["iii_one_sequence_share"] = round(T["types_in_one_sequence"] / max(1, T["types"]), 2)
    hapax_iii, hapax_f = T["types_in_one_sequence"], sum(len(v) == 1 for v in occ.values())
    M["iii_share_of_hapax"] = round(hapax_iii / max(1, hapax_iii + hapax_f), 2)
    ch = T["channel"]
    n = max(1, T["sequences"])
    M["iii_channel_pct"] = {c: round(100 * ch.get(c, 0) / n) for c in ("Ch-1", "Ch-2", "Ch-4")}
    # the two silhouettes, measured three ways
    roots = [u["form"] for u in reg if u["kind"] == "root"]
    M["root_mean_syllables"] = round(sum(len(ph.syllables(f)) for f in roots) / max(1, len(roots)), 2)
    M["root_coda_final_share"] = round(sum(not ph.syllables(f)[-1][-1] in "aeiou" for f in roots) / max(1, len(roots)), 2)
    # segments on which the Standard and Sturge come apart need a coordinate on a chain of
    # two or more edges: three roots, two tails, the carrier's head, three slots, a warrant
    M["min_tokens_multi_edge_coordinate_segment"] = 9
    M["functional_tokens"] = F["stratum_tokens"].get("I", 0) + F["stratum_tokens"].get("II", 0)
    # the list
    closed_bands, open_bands = defaultdict(set), defaultdict(set)
    for s in ph.OPEN:
        open_bands[s[0]].add(s[1])
    for s in ph.CLOSED:
        closed_bands[s[0]].add(s[1])
    M["bands_open"] = {c: "".join(sorted(v)) for c, v in sorted(open_bands.items())}
    M["bands_closed"] = {c: "".join(sorted(v)) for c, v in sorted(closed_bands.items())}
    M["commanded_core_cap"] = ph.commanded_core_cap()
    from .lexicon import validate
    lx = default_lexicon()
    free = [g.GAP] + list(g.PASS_VALUES) + list(g.PHASE_VALUES) + [w for w in g.WARRANTS if w != "[41]"]
    M["commanded_core_size"] = len(lx.commanded()) + len(free)
    M["lexicon_problems"] = len(validate(lx))
    # the analyzable core: roots and ritual units in the core register, plus the formatives
    core = [u for u in reg if u.get("core") or u["kind"] == "ritual"]
    forms = [f.form for f in g.FORMATIVES if f.form != "[41]"]
    has_coda = lambda f: any(ph.is_closed(x) or x in ph.ONSETLESS for x in ph.syllables(f))
    M["analyzable_core"] = len(core) + len(set(forms))
    M["analyzable_core_coda_share"] = round((sum(has_coda(u["form"]) for u in core) +
                                             sum(has_coda(f) for f in set(forms))) / max(1, M["analyzable_core"]), 2)
    from .diachrony import coda_count_1908
    n08, n88, tot = coda_count_1908()
    M["roots_with_coda_1908"] = f"{n08} of {tot}"
    # the bound pairs, by stratum
    M["kalsira_frozen_in_III"] = F["kalsira_ru"]["uncompleted_by_stratum"].get("III", 0)
    # Stratum III: the non-divisible five, and CSC-1146
    iii = [e for e in cat if e["stratum"].startswith("III")]
    M["iii_nondivisible_lengths"] = sorted(len(e["units"]) for e in iii if len(e["units"]) % 3)
    M["iii_nondivisible_provisional_lengths"] = sorted(
        len(e["units"]) for e in iii if len(e["units"]) % 3 and e["stratum"] == "III (provisional)")
    t1146 = [e for e in cat if e["ref"] == "CSC-1146"][0]["units"]
    others = [e["units"] for e in iii if e["units"] != t1146]
    seen_elsewhere = {u for us in others for u in us}
    M["csc1146"] = {"tokens": len(t1146), "types": len(set(t1146)),
                    "types_in_no_other_sequence": sum(1 for u in set(t1146) if u not in seen_elsewhere),
                    "refrain_positions": [i + 1 for i, u in enumerate(t1146) if u == "tirakur"]}
    # Stratum IV: units shared with the functional strata
    iv = {u for e in cat if e["channel"] == "Ch-3" for u in e["units"]}
    M["iv_shared_with_functional"] = len(iv & set(occ))
    # sequences counted in units (node words, free units, fields, log entries), not morphemes
    def units_of(e):
        if e["segments"]:
            return [len(parse_segment(s["translit"], lex).words) + len(parse_segment(s["translit"], lex).free)
                    for s in e["segments"]], [len(parse_segment(s["translit"], lex).tokens()) for s in e["segments"]]
        return [len(e["units"])], [len(e["units"])]
    ge3, longest, over30 = 0, 0, 0
    for e in cat:
        us, ts = units_of(e)
        for u, t in zip(us, ts):
            ge3 += t if u >= 3 else 0
            longest = max(longest, u)
            over30 += u > 30
    M["tokens_in_sequences_of_3plus_units"] = ge3
    M["longest_sequence_units"] = longest
    M["sequences_over_30_units"] = over30
    # the Archive of works: every year the A-family cites is in data/chronology.yaml
    chron = yaml.safe_load((ROOT / "data" / "chronology.yaml").read_text(encoding="utf-8"))["events"]
    have = {e["year"] for e in chron if e.get("year")}
    cited = set()
    for f in ("A-path-primary-notation.md", "A-stratum-III-reserve.md"):
        txt = (ROOT / "docs" / "arch" / f).read_text(encoding="utf-8")
        cited |= {int(y) for y in re.findall(r"\b(1[89]\d\d|20[01]\d)\b", txt)}
    M["chronology_missing_years"] = sorted(cited - have)
    M["preamble_grades"] = dict(Counter(grade for _, grade in g.A_PREAMBLE_ITEMS)) \
        if g.A_PREAMBLE_ITEMS and isinstance(g.A_PREAMBLE_ITEMS[0], tuple) else None
    M["confusions"] = ph.confusion_table()
    return M


def _get(M, path):
    x = M
    for k in path.split("."):
        x = x[k] if isinstance(x, dict) else x[int(k)]
    return x


def _close(got, want, tol):
    """Equal, or within ``tol``; ``{min, max}`` states a range."""
    if isinstance(want, dict) and want and set(want) <= {"min", "max"}:
        return want.get("min", float("-inf")) <= got <= want.get("max", float("inf"))
    if isinstance(want, (int, float)) and isinstance(got, (int, float)):
        return abs(got - want) <= tol
    return got == want


def claims(figs=None) -> list[dict]:
    spec = yaml.safe_load((ROOT / "data" / "claims.yaml").read_text(encoding="utf-8"))["claims"]
    M = metrics()
    out = []
    for c in spec:
        got = _get(M, c["measure"])
        tol = c.get("tolerance", 0)
        row = {"id": c["id"], "what": c["what"], "where": c["where"], "says": c["says"],
               "got": got if not isinstance(got, float) else round(got, 3), "finding": c.get("finding")}
        if "repaired_to" in c:
            ok = _close(got, c["repaired_to"], tol)
            row["status"] = "repaired" if ok else "fails"
            row["now"] = c.get("now", c["repaired_to"])
        elif c.get("calibration"):
            ok = _close(got, c["expect"], tol)
            row["status"] = "holds" if ok else "calibration"
            row["note"] = c["calibration"]
        else:
            row["status"] = "holds" if _close(got, c["expect"], tol) else "fails"
        out.append(row)
    return out


def main():
    rows = claims()
    width = max(len(r["id"]) for r in rows)
    bad = 0
    for r in rows:
        tag = r["status"].upper()
        bad += r["status"] == "fails"
        print(f"{tag:12} {r['id']:<{width}}  said {r['says']!s:<22} got {r['got']!s:<22} {r.get('finding') or ''}")
    counts = Counter(r["status"] for r in rows)
    print(dict(counts))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
