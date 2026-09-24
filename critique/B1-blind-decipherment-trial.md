# B1 — Blind decipherment trial

> **Authority C.** A test of the Phase 2 build, run 24 September 2026. The three raw
> reports are in `critique/B1-trial/`; their catalogue numbers refer to the corpus as it
> stood before the fixes in §4, which renumbered it.

## 1. What was tested

The benchmark's Etruscan condition: **a reader with everything HEL publishes should be
able to recover the structure of the notation and should not be able to recover what it
means.** The sealed key (`sealed/key.yaml`) holds the answers, so for the first time the
condition can be scored rather than asserted.

**The packet** was the published material and nothing else: the catalogue (530
accessions as then built), the unit register, the published figures, the nine formulae,
and the two handbook documents (A and its Stratum III reserve). No generator code, no
sealed file, no Phase 2 documents. The packet was checked for sealed strings before it
was handed over (none).

**The readers** were three independent agents, each told to read only the packet and to
answer nine standing disputes, the ten most frequent roots, `[41]` and Stratum III, with
a confidence for every verdict:

- a **philologist** — distributional and comparative method;
- a **signals engineer** — the notation as a protocol: fields, framing, what varies
  with what;
- a **skeptical auditor** — what the Archive's own transcription and filing produced.

**Compliance.** Every tool call of all three (206 in all) was audited afterwards for
paths outside the packet. There were none.

## 2. Scores against the sealed key

### The disputes

| Dispute | Sealed truth | Philologist | Engineer | Auditor |
| --- | --- | --- | --- | --- |
| Keele 1963: is *kalsira-ru* frozen? | yes | **yes** 0.9 | **yes** 0.85 | **yes** 0.8 |
| Redfern 1993: is ADJ a damage convention? | yes | **yes** 0.85 | **yes** 0.9 | **yes** 0.9 |
| Locative or Stative roots? | Stative | **Stative** 0.65 | **not places** 0.7 | **not places** 0.75 |
| The Ladder: Cardwell or the Long Reading? | Cardwell | **Cardwell** 0.65 | **leans Cardwell** 0.6 | undecidable, leans Cardwell |
| Onslow 1971: one class or two? | two | undecidable, leans two | **two** 0.65 | undecidable |
| Hallam 1976: junction or record-stop? | split: junction on Ch-1 objects, page-end mark on Ch-2 hand copies | Ch-1 half only | Ch-1 half only | Ch-1 half only |
| The 1969 *lartuki-halu* paraphrase | form right, content wrong: nothing lapsed | form right; "cessation" 0.6 — **wrong** | form right; "lapsed" unsupported | **form right; "lapsed" unsupported and weakly contradicted** |
| REG, 1949 | both glosses wrong: the record was made remote from what it describes | leans to the old gloss | leans to the old gloss | the new gloss, minus "human" |
| **Sturge 1958** (undecidable by construction) | **no fact of the matter** | **undecidable** 0.85 | **undecidable** 0.75 | **undecidable** 0.75 |

**Five disputes are recoverable from the catalogue and were recovered**, by at least two
readers each, with the right side and usually the right mechanism. **Three were
partially recovered**: every reader got Hallam's Ch-1 half and none got the Ch-2 half;
the *lartuki-halu* content was read correctly by one. **One was not recovered by
anyone** (REG), and it is the one whose evidence is not in the published catalogue at
all: whether a record was made at or away from what it describes is a fact about the
sealed world, and the catalogue gives find loci, not described loci.

**The designed undecidable stayed undecidable.** All three readers said Sturge cannot be
settled, for the reason the key gives: no magnitude is anywhere.

### The roots

**Nothing recovered.** All three concluded, independently and with statistics, that root
meanings cannot be recovered from this corpus — only distributional roles. The
philologist ran about 800 root-by-feature tests and found that nothing survives
correction except the two bound pairs. The sealed key's 43 root correlations stayed
sealed. This is the Etruscan condition holding where it matters most.

### Stratum III

**Form recovered; meaning not; no reading attempted beyond what the evidence allows.**
All three reduced the 79 sequences to about twenty repetition templates in a handful of
families — refrain triads, mirrors, envelopes — which is the composition procedure in the
sealed PRODUCTION register, found from outside. All three said no reading is supportable.
The auditor added that the templates recur across 31 loci, three channels and 150
years, so the reserve's "no cross-record repetition" is true of units and false of form —
a fair correction of the reserve's rhetoric, and one the class survives.

### `[41]`

**A production leak.** All three found that on Ch-1 objects `[41]` occurred only on
closure records (three of three, BAR or FRB; p ≈ 5×10⁻⁵), and two read it as a closure
warrant. The sealed rule for `[41]` has no truth value — *placed in every formula and on
three Ch-1 objects* — so any pattern it shows is an accident of placement, and the
handbook says `[41]` must never be explained. It was an accident: the build placed it on
three status records. **Fixed** (§4).

The engineer also found that the ritual unit before `[41]` co-varied with polarity:
*tuwalsi* ended exactly the two formulae with a negative polarity. The ritual units are
placed by the metre and nothing else. **Fixed** (§4).

## 3. What the readers found that nobody asked them to

**The Archive's damage model is wrong, and its own catalogue says so.** All three found
it independently. The catalogue's condition field separates damage from grammar almost
perfectly: of the 101 segments then ending in a broken half, 66 were the three identified
constructions — the 24 frozen *kalsira-ru*, the 19 *lartuki-halu*, the 23 half-negated
tails — all on intact, warranted objects, and every other break was on a worn, fractured
or eroded object. True damage was about 8% of segments, against the figures' 24% and the
handbook's 41%. ADJ occurred only on damaged objects and produced every ill-formedness
finding in the catalogue.

Part of that is in-world and right: the Archive's broken-half figure has never been
re-audited (A §4.2 says so), and a catalogue that still counts Keele's pairs as breaks is
the institution behaving as described. **Part of it was the engine**: it flagged the
Archive's own identified constructions as damage (`D-BROKEN`) sixty years after Keele.
That is a build defect, and it is fixed (§4).

**The re-audit found nothing, and it should have.** The sealed key says nine further bound
pairs are hidden in the break inventory, rendered as uncompleted tails and not yet
identified by HEL. All three readers re-ran Keele's method — bare tails on intact
warranted objects — and the engineer concluded that "the break inventory hides no
further frozen pairs". **He was right about the build**: the nine had never been
rendered. The sealed key promised data that did not exist. **Fixed** (§4): the nine are
now in the corpus, and Keele's method, applied by anyone, will find them.

**Glosses without records.** The auditor found eight glossed roots that never occur in the
catalogue and five that occur only in HEL's own formulae; the engineer showed the formula
glosses tracking the formulae's occasions. The second is in-world and damning in the right
way — the Archive glossed ritual units from the rituals. The first is a build defect: a
gloss graded by operational correlation needs records to rest on. **Fixed** (§4).

**Other points the documents should hear:** the shadow segments (A §5.5), which the
Archive explains away as misparsed damage, are complete, warranted records on intact
objects, so the deflation is refuted by the catalogue — an in-world argument the
Archive loses, left standing; the "100% head-bearing carrier" figure is kept at 100% by
filing the counterexamples, which are all ADJ-damaged, as ill-formed (compare F-07);
and the Hallam split's evidence — page-end *-ar* in pre-photographic hand copies — rests
on 15 hand copies carrying 2 *-ar* tokens between them, too few to find. That last is a
calibration fault in the build, not a failure of the readers.

## 4. Fixes made because of the trial

| Defect | Fix |
| --- | --- |
| `[41]` on three closure records | placed on three records of unrelated kinds with no polarity (two labels and a BIND record), from a separate random stream |
| ritual units co-varying with polarity | the sealing and the reading-room opening swap ritual units; each ritual unit now ends formulae of mixed polarity |
| the nine unpublished bound pairs never rendered | listed in the sealed key (TRUTH) and rendered, two of each, bare and where their condition holds — findable by Keele's method |
| identified constructions flagged as damage | catalogued as `N-PAIR` and `N-HALFNEG` notes; the figures split broken halves into constructions and the rest |
| glossed roots with no records | every glossed root occurs at least twice, at a node and pass where its condition holds |

**Not re-run blind.** The fixes remove the specific patterns the readers found; a second
trial on the corrected corpus would test whether they introduced others. Recommended
before any of this goes further.

## 5. Verdict

The Etruscan condition holds for what it was designed to protect: **no root meaning, no
Stratum III reading, and no answer to the undecidable dispute** came out of the packet.
The notation's structure came out, and so did the answers to five disputes the world
really does decide — which is what the design wants: a reader who works hard should be
able to correct the Archive where the Archive is wrong, and should not be able to read
the substrate. The trial's real yield was the four production leaks and gaps, each of
which a player with a spreadsheet would eventually have found.
