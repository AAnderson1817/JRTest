#!/usr/bin/env python3
"""Regression lint for the CSC flagship text.

Reads the transliteration block out of A-stratum-III-reserve.md §8.1 rather than
taking a hardcoded copy, so the document stays the single source of truth, and
checks every structural invariant §8.2 claims about it.
"""
import re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from syllabary import segment, CLOSED, ONSETLESS

DOC = pathlib.Path(__file__).parent.parent / "docs/arch/A-stratum-III-reserve.md"
text = DOC.read_text(encoding="utf-8")

# §8.1 transliteration block: three '> ' lines of units joined by '·'
m = re.search(r"\*\*Transliteration \(layer 2\).*?\n\n((?:> .*\n){3})", text)
if not m:
    sys.exit("LINT ERROR: could not locate the §8.1 transliteration block")
seq = [u.strip() for line in m.group(1).strip().split("\n")
       for u in line.lstrip("> ").split("·")]

fails = []
def check(cond, label, detail=""):
    print(("  ok   " if cond else "  FAIL ") + label + (f"  — {detail}" if detail and not cond else ""))
    if not cond:
        fails.append(label)

print(f"sequence read from {DOC.name} §8.1:\n  " + " · ".join(seq) + "\n")

# 1. every syllable on the 1908 sanctioned list
segs = {}
for u in seq:
    s = segment(u)
    if not s:
        fails.append(f"{u} not on sanctioned list")
        print(f"  FAIL {u}: not built from the §6.1b list")
    else:
        segs[u] = s
check(len(segs) == len(set(seq)), "all units segment under the 1908 sanctioned list (§6.1b)")

types = list(dict.fromkeys(seq))
syl = sum(len(segs[u][0]) for u in seq)

check(len(seq) == 9, "9 tokens", f"got {len(seq)}")
check(len(seq) % 3 == 0, "token count divisible by 3 (§4.1)")
check(len(types) == 6, "6 types", f"got {len(types)}")

refrain = [t for t in types if seq.count(t) == 3]
check(len(refrain) == 1 and [i for i,u in enumerate(seq) if u == refrain[0]] == [2,5,8],
      "refrain ×3 at group-final positions 3, 6, 9")
env = [t for t in types if seq.count(t) == 2]
check(len(env) == 1 and [i for i,u in enumerate(seq) if u == env[0]] == [0,6],
      "envelope type ×2 at positions 1 and 7")

# terminal-syllable scheme
term = [segs[u][0][-1] for u in seq]
g = [term[0:3], term[3:6], term[6:9]]
check(g[0] == g[2], "groups 1 and 3 share an identical terminal scheme", f"{g[0]} vs {g[2]}")
check(sorted(x[-2:] for x in g[1]) == sorted(x[-2:] for x in g[0]),
      "group 2 is a transposition of the same three terminals")

# §6.1c: 3+ syllables ⇒ at least one coda; and every token here ends in a coda
coda = lambda s: s in CLOSED or s in ONSETLESS
check(all(len(segs[u][0]) < 3 or any(coda(x) for x in segs[u][0]) for u in seq),
      "§6.1c minimum coda rate")
check(all(coda(segs[u][0][-1]) for u in seq), "9 of 9 tokens end in a coda")

# distinctness violation, deliberate and singular
firsts = [segs[t][0][0] for t in types]
dupes = {f for f in firsts if firsts.count(f) > 1}
check(len(dupes) == 1, "exactly one shared first syllable (the deliberate §6.1e violation)",
      f"shared: {dupes or 'none'}")

# the 1971 argument needs exactly three types carrying the string 'ar'
ar = [t for t in types if "ar" in t]
check(len(ar) == 3, "exactly 3 types contain the string 'ar' (§8.2, 1971 proposal)", f"got {ar}")
amb = [t for t in types if len(segs[t]) > 1]
check(len(amb) == 1 and amb[0] in ar,
      "exactly one type is segmentation-ambiguous, and it carries 'ar'", f"got {amb}")

# mean syllables, as printed in the §8.2 table
mean = syl / len(seq)
s82 = text[text.index("### 8.2"):] if "### 8.2" in text else text
printed = re.search(r"\| Mean syllables per unit \| ([0-9.]+)", s82)
check(printed is not None and abs(float(printed.group(1)) - mean) < 0.05,
      f"§8.2 printed mean matches computed {mean:.2f}",
      f"printed {printed.group(1) if printed else '?'}")

# the seven coined forms declared in §10 are exactly the 6 types + the 1939 variant
declared = re.search(r"on the seven forms coined in this file — (.*?) — plus", text, re.S)
if declared:
    names = re.findall(r"`([a-z]+)`", declared.group(1))
    check(set(names) == set(types) | {n for n in names if n not in types} and len(names) == 7,
          "§10 screen statement declares 7 forms")
    check(set(types) <= set(names), "§10 declares every type used in §8.1",
          f"missing {set(types) - set(names)}")
    for n in names:
        if not segment(n):
            fails.append(f"§10 declared form {n} off-list")
            print(f"  FAIL §10 form {n} is not on the sanctioned list")
    check(all(segment(n) for n in names), "every §10 declared form is on the sanctioned list")
else:
    check(False, "§10 screen statement parseable")

# --- §4.2 / §3.3 corpus arithmetic ------------------------------------------
# The hapax share claimed in §3.3 prose must follow from the §4.2 table.
t3   = re.search(r"\| Distinct types \| (\d+) \| ~(\d+) corpus-wide \|", text)
hap  = re.search(r"\| Types occurring in exactly one sequence \| \*\*(\d+) \((\d+)%\)\*\* \| ~(\d+)% \|", text)
if t3 and hap:
    iii_types, fn_types = int(t3.group(1)), int(t3.group(2))
    iii_hapax, iii_pct, fn_pct = int(hap.group(1)), int(hap.group(2)), int(hap.group(3))
    check(abs(iii_hapax / iii_types * 100 - iii_pct) < 1,
          f"§4.2 hapax rate {iii_hapax}/{iii_types} matches printed {iii_pct}%")
    fn_hapax = fn_types * fn_pct / 100
    share = iii_hapax / (iii_hapax + fn_hapax) * 100
    claimed = re.search(r"holds about ([a-z-]+|\d+%) of the whole corpus's hapax units", text)
    word = {"two-thirds": 66.7, "half": 50.0, "a third": 33.3}
    got = claimed.group(1) if claimed else None
    val = word.get(got, float(got[:-1]) if got and got.endswith("%") else None)
    check(val is not None and abs(val - share) < 5,
          f"§3.3 hapax share claim matches computed {share:.0f}%", f"prose says {got!r}")
else:
    check(False, "§4.2 corpus-arithmetic rows parseable")

print()
if fails:
    print(f"FAILED — {len(fails)} check(s): " + "; ".join(fails))
    sys.exit(1)
print("PASS — flagship text conforms to §6.1b–e and every §8.2 claim.")
