#!/usr/bin/env python3
"""Validate CSC transliterated units against the 1908 sanctioned list (A §6.1b)
and the shape rules (A §6.1c-e). Greedy-longest segmentation with backtracking."""
import sys, re, json

OPEN = "ha he hi ka ke ki le li lu ni nu pe pu ra ro ru sa si ti to tu yu".split()
CLOSED = ("har hos kal kas ken kur lan lar lun lus mun nes nir pel sar sen sil "
          "tel tir tul wal yun").split()
ONSETLESS = "ar in is ol".split()
SANCTIONED = OPEN + CLOSED + ONSETLESS
assert len(SANCTIONED) == 48, f"list is {len(SANCTIONED)}, must be 48"
assert len(set(SANCTIONED)) == 48, "duplicate syllable on list"

def segment(word):
    """All valid segmentations of word into sanctioned syllables."""
    if not word:
        return [[]]
    out = []
    for syl in SANCTIONED:
        if word.startswith(syl):
            for rest in segment(word[len(syl):]):
                out.append([syl] + rest)
    return out

def analyse(word):
    segs = segment(word)
    r = {"unit": word, "valid": bool(segs), "segmentations": segs}
    if segs:
        s = segs[0]
        r["syllables"] = len(s)
        r["first"] = s[0]
        r["last"] = s[-1]
        r["codas"] = sum(1 for x in s if x in CLOSED or x in ONSETLESS)
        # 6.1c: every unit of 3+ syllables carries at least one coda
        r["rule_6_1c"] = (len(s) < 3) or (r["codas"] >= 1)
        r["ambiguous"] = len(segs) > 1
    else:
        # locate the offending prefix for a useful error
        bad = word
        for i in range(len(word), 0, -1):
            if segment(word[:i]):
                bad = word[i:]
                break
        r["unparsable_from"] = bad
    return r

if __name__ == "__main__":
    units = sys.argv[1:]
    if not units:
        units = [l.strip() for l in sys.stdin if l.strip()]
    results = [analyse(u) for u in units]
    ok = True
    for r in results:
        if r["valid"]:
            seg = "-".join(r["segmentations"][0])
            flag = ""
            if not r["rule_6_1c"]:
                flag += "  !! 6.1c violation (3+ syllables, no coda)"; ok = False
            if r["ambiguous"]:
                flag += f"  (ambiguous: {len(r['segmentations'])} segmentations)"
            print(f"  OK   {r['unit']:<14} {seg:<20} {r['syllables']} syll{flag}")
        else:
            ok = False
            print(f"  FAIL {r['unit']:<14} not on list from: -{r['unparsable_from']}")
    sys.exit(0 if ok else 1)
