# Blind decipherment trial: report of the philologist

Sources: only the published packet (`archive-handbook-A.md`, `archive-handbook-stratum-III.md`, `catalogue.json`, `register.json`, `figures.json`, `formulae.yaml`). Scripts and intermediate tables are in `work-philologist/`. Catalogue references are CSC numbers; "St" is the catalogue's stratum; "profile" is the catalogue's per-segment formal profile.

---

## 0. Before the disputes: the data, and two warnings about the handbook

**The parse.** I parsed all 417 functional segments morpheme by morpheme. I used the transliterations and the Archive's aligned gloss lines, slot by slot: head, root, incidence, tail, grade, the unlisted post-grade slot, polarity, post-polarity slot, `-he`, coordinate and warrant. Every segment reassembles to its transliteration. The only mismatches are the 34 stacked warrants, which is the published figure. Every number in `figures.json` that I tested reproduces from this parse: 4,016 tokens, 101 segments with a flagged broken half, 54 SHUNT/RECUR edges, 18 ADJ halves and 0 ADJ pairs, 27 kalsira-ru, 19 lartuki-halu, 23 tail-only `-mun`, 12 multi-edge coordinate segments, and 79 Stratum III sequences with 707 tokens. So the catalogue and the figures agree with each other. **The handbook does not agree with either:**

| Handbook says | Catalogue / figures show |
|---|---|
| ~41% of sequences end in a broken half (§4.2, §5.5) | 101/417 = 24%; genuine damage 35/417 = 8% (below) |
| 214 junction-map nodes, ~60% junction by `-ar` alone (§4.6b) | 157 nodes, 153 (97%) by `-ar` alone |
| 87 ADJ-only edges (§4.6c) | 18 ADJ halves |
| ~380 SHUNT/RECUR edges (§4.6a) | 54 |
| Longest sequence 41, six over 30 (§2.3) | longest 25, none over 30 |
| Stratum II environments 212 / 148 / 63 / 85 / 31 (§7.1) | 24 / 13 / 4 / 9 / 3 (older-branch cut present: 2) |
| Aubrey: RECUR sits on `-is` MED nodes (§4.6a) | RECUR is never on a MED node (0/23) |
| Vance: no I–III object bears both SHUNT and RECUR | CSC-1253 does (via the frozen lartuki-halu) |
| `-he` "throughout Stratum I", "absent from Stratum II entirely" (§4.4, §7) | on 6 of 21 polarity tokens on St I objects; present on St II object CSC-1479 |
| lartuki-halu is "the nearest the corpus comes to expressing a lapse" (§10.1b) | the catalogue itself glosses `-sar` LAPSED, 8 tokens |

**The paradigm tables are not the catalogue's paradigm.** PREP `-ka` and UNV `-lus` (both graded G1 in §4.3/§4.4) occur nowhere in Strata I–II. They are attested only as free units in Stratum IV (ka 4, lus 9). Conversely, the catalogue attests 44 tokens of formatives the handbook never tabulates:
- a slot after the grade: `-lun` STANDING? (20), `-sar` LAPSED (8), `-ro` SPENT (1). It occurs only after EXEC or AUTH.
- `-lar` UNENT? (2), only after AUTH.
- a slot after the polarity: `-kur` EVERY (12), `-li` ONCE (1).

These account exactly for the figures' "imports" (29 / 2 / 13). I use the catalogue, not the handbook, throughout.

**The one diagnostic that does most of the work below: damage has a clean signature.** Every one of the 320 segments on intact objects carries a warrant. On damaged objects only 34 of 88 do (worn 25/37, fractured 9/38, eroded 0/13). Of the 101 segments the catalogue flags `D-BROKEN`, two groups separate completely:
- **35 are damage.** All sit on worn, fractured or eroded objects, and 32 of them have also lost their warrant.
- **66 are not damage.** All sit on intact objects and all are warranted: every kalsira-ru (24), every lartuki-halu (19) and every tail-only `-mun` (23).

No intermediate case exists.

---

## A. The disputes

### 1. Onslow (1971): SHUNT and RECUR, one class or two?
**Verdict: undecidable from this corpus, with a weak lean to two classes (side 2). Confidence 0.6 that it is undecidable; 0.55 for the lean.**

- **Too little RECUR to test.** Outside the frozen lartuki-halu, RECUR has 5 edges: CSC-1001 (a Ch-4 formula), CSC-1193, CSC-1325, CSC-1410, and CSC-1418, a lone head on a fractured object. SHUNT has 30. No minimal pair exists in Strata I–III.
- **The Archive's standing defence is false here.** Aubrey says SHUNT sits on TERM and RECUR on MED. The SHUNT tail-bearers are TERM 18, MED 7, JCT 4. RECUR tail-bearers are TERM 21/23 (19 of them lartuki-halu), JCT 1, none 1, and never MED. The two classes are not in complementary distribution by incidence: both occur on TERM and JCT origins and TERM destinations. That fits two contrasting classes and one freely-varying class equally well.
- **Vance's claim fails only trivially.** The only I–III object with both tails is CSC-1253 (`harhape-in-tul · tu-lartuki-in-halu`). Its RECUR is the frozen pair, not a productive edge.
- **The Stratum IV "contrasts" cannot carry the argument.** Records CSC-1522 and CSC-1526 do show both `tul` and `halu` in slot 2 of Stratum IV's triplets. But Stratum IV uses the shared inventory with a frequency profile unrelated to Strata I–II: Spearman ρ = −0.02 over 32 formatives. `in` occurs 391 times in I–II and 4 in IV; `hos`/`lekur`/`wal` are absent from IV; `lus` is 0 in I–II and 9 in IV. That is what the Palimpsest reading predicts, so the IV contrast proves nothing about I–III.
- **The lean.** Onslow's mechanism is two nineteenth-century register traditions merged in 1908. That mechanism does not explain why the Archive keeps assigning both tails to objects recovered after 1908. Productive RECUR appears on accessions of 1912, 1943, 1965 and 1966, and 14 of the 19 lartuki-halu were catalogued after 1908. The frozen pair is `-halu` 19/19, never `-tul`. This is weak evidence: it depends on unstated transcription practice. The catalogue does not record which register tradition any transcription came from, and that is the variable Onslow needs.

### 2. Hallam (1976): does `-ar` mark a junction, or that the record stops?
**Verdict: side 1, a junction (the Standard). Confidence 0.65.**

Every piece of evidence the handbook credits to Hallam fails to replicate in the published catalogue:
- **Damage.** `-ar` is *under*-represented on damaged objects: 23/154 (14.9%), against TERM 25.6%, OFF 25.6% and MED 44.7%.
- **Broken halves.** Only 4 of the 149 segments containing `-ar` have a flagged break (2.7%), against 97 of 268 segments without it (36.2%). All four are on damaged objects (CSC-1270, 1296, 1302, 1332).
- **Margins.** In segments of three or more node words, `-ar` is interior 16/23 times (70%), against 42/127 (33%) for other node words. It is the reverse of marginal.
- **Hand copies.** Page ends are not recorded, so her page-end claim cannot be tested. But `-ar` is rarest in the pre-photographic hand copies: 2/23 node words (8.7%), against Ch-1 objects 27.5% and Ch-2 plates 17.2%.
- **Positive evidence for JCT.** 12 `-ar` nodes are chain-medial, so the record demonstrably continues through them (for example CSC-1065, CSC-1108, CSC-1200, CSC-1465). The only node in the catalogue whose additional edges are visible is `yunpuru` on CSC-1065. It is `ru-yunpuru-ar-ru` in segment 1 (in-edge plus out-edge), and segment 2 of the same object adds a third edge, `yunpuru-in-ru-kas-lun → isruyu`. It carries `-ar` exactly where its other edge goes unstated.

**Residue.** Whether the unstated edges exist in the network cannot be checked beyond CSC-1065. No `-ar` label root recurs at its own find locus (0/121). A weak Hallam ("the account of this node is incomplete here") is nearly indistinguishable from JCT, but the record-incompleteness version she argued is not supported.

### 3. Redfern (1993): is ADJ an edge class, or a damage convention?
**Verdict: side 2, a damage convention. Confidence 0.85.** One caveat on "nineteenth-century": the corpus shows a convention the Archive still applies, not one confined to the nineteenth-century registers.

- **Condition.** All 18 ADJ halves sit on damaged objects: 15 objects, of which 6 worn, 5 eroded and 4 fractured. The baseline is 81% intact (307/378 written entries with segments), so chance gives p ≈ 0.19^15 ≈ 10^-11. Every other edge class occurs mostly on intact objects.
- **No head, and uniquely so.**
  - No `yu-` head exists anywhere (0/18).
  - ADJ is the only class ever headless before a consonant-initial root (8 cases).
  - It never takes grade or polarity (0/18). PASS tails take one 40% of the time (81/203), SHUNT 41% and THRU 60%.
- **The next word behaves like a destination whose head is lost.** All 8 `E-CARRIER` findings are words right after an ADJ mark that carry a coordinate without a head: CSC-1049, 1054, 1124, 1126, 1341 ×2, 1409 and 1552. All 3 `E-OFF` findings are ADJ into an OFF node (CSC-1049 ×2, CSC-1362). **Every one of the catalogue's 11 ill-formedness findings sits in an ADJ segment**, and 13 of the 18 ADJ segments have also lost their warrant.
- **It breaks Stratum I's own profile.** CSC-1414 has an ADJ in a profile-I segment, where "both edge halves always overt".
- **Corroboration from Stratum IV (weak, and valid only if IV is the same system).** The undamaged instrument channel attests six edge-tail shapes (`ru` 44, `ken` 13, `tul` 12, `halu` 5, `pel` 4, `sil` 3) and never `yun`.
- **Dates.** ADJ objects were accessioned from 1886 to 2023; CSC-1552 was accessioned and catalogued in 2023. So whatever its origin, the convention is still being applied, and applied only to damaged surfaces.

### 4. The Ladder plaque: is `-sen` segment-scoped (Long Reading) or edge-scoped (Cardwell)?
**Verdict: side 2, edge-scoped (Cardwell). Confidence 0.65.**

The plaque itself cannot decide: CSC-1165 is single-edge. The corpus, however, decides the general rule:
- **Stratum II marks polarity edge by edge,** several times per segment. CSC-1337 has `-nir`, `-sen` and `-nir` on edges 1, 2 and 4 of a four-edge chain, and the chain continues past the `-sen` edge to a coordinate (`to-kihar`). CSC-1328 has `-nir-kur` on edge 1 and `-sen-kur` on edge 2. UNA asserts "not closed". A segment-scoped FRB would contradict the UNA-marked edges of the same segment. So in the only Stratum II segments where scope is testable, FRB without `-he` is edge-scoped.
- **Nowhere does a polarity have to be read with segment scope.** Every polarity in a multi-edge Stratum I chain carries `-he`: CSC-1173 (two), CSC-1289.
- **The `-he` contrast is not what the handbook says it is.**
  - `-he` occurs on 7 of 62 polarity tokens: FRB 4 (CSC-1289, 1313, 1352, 1479) and UNA 3 (CSC-1173 ×2, 1339). It occurs on IMP 0 of 24 times.
  - On Stratum I objects it is on 6 of 21 polarity tokens. FRB occurs without it on St I object CSC-1200 (`lunkinu-in-tul-sen`).
  - It does occur in Stratum II (CSC-1479).
  - The absence of `-he` is therefore not a marker of segment scope. The "structural ambiguity" of the plaque rests on a stratal contrast the catalogue does not show.
- **No contrary parallel.** The Ch-4 sealing formula (CSC-1012, `nirtoka-pel-sen · pe-olsihe-in`) has the plaque's structure and says nothing against this.
- I found no evidence for the Hallam "fourth reading" (see dispute 2).

### 5. Keele (1963): is kalsira-ru a frozen pair, or a literal onward PASS edge?
**Verdict: side 1, frozen. Confidence 0.9.**

- **None of the 24 is damage.** All 24 uncompleted kalsira-ru are Stratum II, on intact objects, and warranted. Each is the only flagged break on its object. 11 are followed by a Stratum III field, which by definition begins after a *completed* segment (CSC-1038, 1061, 1153, 1158, 1160, 1247, 1360, 1408, 1432, 1472, 1510). The Archive's own catalogue still flags all 24 as `D-BROKEN … damaged`.
- **Morphology.** The 24 are the only tail-bearing words in Ch-1 and Ch-2 that lack an incidence marker; every other written node word has one. `-ru` stands where Stratum I puts `-in`:
  - Stratum I: `ru-kalsira-in` (CSC-1191).
  - Stratum II: `ru-kalsira-ru` (CSC-1038, 1088, 1160, 1360, 1432, 1459), `ke-kalsira-ru` (CSC-1300), `tu-kalsira-ru` (CSC-1472).

  The completed Stratum I tokens are regular `kalsira-in-ru · ru-X` (CSC-1407, 1448, 1460). This supports the attested reading: traversal reaches CSC-0012 and goes no further.
- **Its company.** kalsira-ru patterns exactly with the tail-only `-mun` statements ("no edge departs") and with lartuki-halu: intact, warranted, headless, and followed by Stratum III at 35–46% (section D).
- **Caveat.** This establishes the frozen status synchronically. It does not establish lexicalization *from* a compositional source: Stratum I and II accession dates interleave completely (medians 1941 and 1938), so no ordering is available.

### 6. Sturge (1958): is the coordinate measured from the preceding tail-bearer or from the chain-initial node?
**Verdict: undecidable from this corpus. Confidence 0.85.**

- 17 coordinate carriers sit on multi-edge chains. The Archive counts 12, excluding chains through ADJ or head-absent links.
- Their PHASE values are pukal 6, kihar 4, nikur 1 and hilun 6. No magnitude appears in any of the corpus's 115 coordinates.
- The cartouche's position identifies only the carrier. PASS and PHASE distributions on multi-edge chains show nothing that one reading predicts and the other does not.
- One case, CSC-1299 (SHUNT leg then PASS leg, PHASE `kihar`), is slightly more natural under the Standard. It is anecdotal.

### 7. The 1969 lartuki-halu paraphrase: right or wrong?
**Verdict: right as far as the corpus can test it, which is not all the way.**
- "No edge is claimed": right, confidence 0.85.
- It is a cessation-type statement rather than a recurrence: supported, confidence 0.6.
- "Attendance … lapsed": untestable.

- **Form.** All 19 have the same shape: `EDGE-lartuki-in-halu=hilun-nu-hilun` plus a warrant (`tir` 12, `nes` 7). All are intact and warranted, and a head is never supplied. `lartuki` is marked TERM (end of chain) while bearing an incoming head, so the `-halu` cannot open an onward edge inside the chain.
- **Its coordinate is the closure coordinate.** `hilun-nu-hilun` occurs 26 times. Outside the pair it appears on 4 of the 5 coordinate-bearing BAR edges (CSC-1012, 1121, 1165, 1554), on all 3 coordinates whose anchor bears FRB (CSC-1012, 1165, 1325), and on the one AUTH-LAPSED segment (CSC-1447). Ordinary traversals take `pukal`/`kihar`/`rolun`.
- **Its company.** Like kalsira-ru and the `-mun` tails it attracts Stratum III fields (6/19). It behaves like a statement that something stopped, not like a return.
- **What cannot be tested.** `lartuki` occurs outside the pair only in the custodial formula (CSC-1002), so "attendance" has no independent support. The corpus has its own LAPSED exponent, `-sar` (8 tokens, e.g. CSC-1065, 1345, 1536), and it never occurs with lartuki. The paraphrase's direction fits; its words cannot be checked.

### 8. Locative vs Stative: do roots name places or states?
**Verdict: side 2, Stative. Confidence 0.65.**

- **Roots do not track places.** The frequent roots are spread over as many find loci as they have tokens: kalsira 29 tokens at 26 loci, lartuki 19 at 19, arhesi 12 at 12, kastuhe, silipelka and kihetirlu 8 at 8 each. A permutation test of same-root/same-locus pairs gives 8 observed against a null mean of 4.9 (p = 0.12). The 8 pairs are:
  - kalsira-ru ×3 at L-16 (Quiet Sixteen) and ×2 at L-14;
  - `lusnuhe-in-ru-mun` ×2 at L-175;
  - one pair each for larluki, rusilke and walpu.
- **The sharpest test: label objects**, a single node word plus warrant. 67 pairs of labels were found at the same locus, and **none shares a root**. Chance predicts 0.3. A reading in which labels name their find-site predicts about 67. Label roots recur only at different loci: kastuhe 5 labels at 5 loci, kihetirlu 5 at 5, arhesi 4 at 4.
- **BIND.** BIND ("same coordinate under two descriptions") always pairs two distinct roots (11 pairs), and `siro` is bound to two different partners (CSC-1200, CSC-1552). That is natural for states and awkward for names.
- **A self-edge that is not a loop.** CSC-1147 has a PASS edge between two nodes bearing the same root (`arpepu-in-ru · arpepu-is-ru`).
- **Residue.** A Locative reading in which labels name *other*, remote nodes cannot be excluded without an independent gazetteer, and objects may have moved.

### 9. The 1949 restyling of REG (`nes`): "registered by the system itself" or "entered without a human attestor"?
**Verdict: split, leaning to the older gloss's positive sense (side 1). Confidence 0.55.** The distribution says `nes` is a specific positive provenance type, not a residual "no human" category. Nothing in it identifies the registrar as "the system itself".

- **`nes` avoids closures.** It is on 0 of the 18 warrants of closure or authorization records (FRB, BAR, AUTH). Its base rate is 29.6%, so chance gives p ≈ 0.002. Those records take `hos` 8, `[41]` 3, `lekur` 3, `tir` 3 and `wal` 1. So `tir` is not excluded from closures, but `nes` is.
- **`nes` is enriched on executions and models.** It is 16 of 36 warrants on EXEC- or SIM-graded records (44%, p ≈ 0.04). `tir` never occurs on SIM, while `nes` does (CSC-1034, 1035, 1139, 1197, 1295, 1556).
- **`nes` never stacks.** It stacks 0 times in 29 Stratum I uses, where 34 stacks occur. `tir` stacks 4/15.
- **Reading.** "Entered without a human attestor" predicts `nes` wherever no human attested and nothing more specific applies. It gives no reason why closures would never take it. A registration category tied to executed and modelled traversals, complementary with `[41]` on closures, fits the pattern better.

---

## B. Roots: the most frequent in Strata I–II

Counts are tokens in Strata I–II, including the Ch-4 formulae catalogued there. Ranks 7–13 are a seven-way tie at 7 tokens, so all thirteen are given. Only two roots have distributions that differ from chance, and both because of their bound pairs. Across roughly 800 root×feature tests, nothing else survives correction.

| Root (CSC) | Tokens / loci | What the evidence shows | Archive gloss | Assessment |
|---|---|---|---|---|
| kalsira (0012) | 29 / 26 | 24 frozen `kalsira-ru` (terminus of sanctioned passage). In Stratum I, 4/4 uses are PASS routes (out: CSC-1407, 1448, 1460; in: CSC-1191), all warranted `tir lekur`, the corpus's only four such stacks (p = 3×10⁻⁴). Stratum III follows 12 of its 27 objects (p = 4×10⁻⁵). All intact. Never FRB, BAR, IMP or UNA. | "sealed" (G3) | **Partly right at best.** "Sealed" describes the bound pair's terminal use, not the root. Productively, kalsira is a repeatedly witnessed departure point of sanctioned routes, which "held closed" does not predict. |
| lartuki (0077) | 20 / 19 | 19 are the frozen lartuki-halu (closure coordinate, see A7); the other is the custodial formula CSC-1002. No independent distribution. | "attendance" (G3) | **Untestable.** It rests on the formula's use-context and the 1969 paraphrase, both HEL practice. |
| arhesi (0038) | 12 / 12 | 4 `-ar` labels, 6 origins (PASS 5, THRU 1). Only reached without a written head (CSC-1124 and CSC-1341 after ADJ; CSC-1132 Stratum II). One FRB with `[41]` (CSC-1128). No association. | "common" (G3) | **Unsupported.** True only trivially (frequent, dispersed); there is no evidence of a state. |
| kastuhe (0039) | 8 / 8 | 5 labels. Reached by SHUNT (CSC-1341) and PASS (CSC-1414). Origin of a shadow segment (CSC-1197). | none (G1) | Correct to offer none; nothing would support one. |
| silipelka (0076) | 8 / 8 | 4 labels. Reached by SHUNT (CSC-1470, `nikur`) and PASS (CSC-1369, `rolun`). Origin of SHUNT (CSC-1200) and of a lartuki-halu (CSC-1454). Fills a LOCUS slot (CSC-1193). | none | As above. |
| kihetirlu (0079) | 8 / 8 | 5 `-ar` labels. BIND origin (CSC-1471), PASS origin into lartuki-halu (CSC-1473), PASS destination (CSC-1395), LOCUS slot (CSC-1536). `tir` 5/8, not significant. | none | As above. |
| harnuli (0007) | 7 / 5 + Ch-4 | Never a destination. All 5 chain uses are origins: the departure formula CSC-1010, the long word CSC-1003, THRU in CSC-1191, the Ladder CSC-1165, SHUNT in CSC-1530. The rest are 2 labels. Two of its five chains go to kurhali. | "in.standing" (G3) | **Untestable.** The one regularity (always an origin, including of the departure formula) is compatible with the gloss but does not discriminate it. |
| yunpuru (0011) | 7 / 6 | PASS origin 6/7. SIM on 3 (CSC-1033, 1172, 1299; p = 6×10⁻⁴, marginal after correction). `hos` 5/7. The one demonstrable junction (CSC-1065). | none | No gloss. At most it correlates with modelled or inferred departures. |
| arhisa (0021) | 7 / 7 | 3 labels; FRB mid-chain (CSC-1337); a destination (CSC-1372). | none | Nothing. |
| kurhali (0104) | 7 / 7 | All Stratum II. Never the origin of a traversable edge: both PASS tails are IMP (CSC-1223, 1388), and the other tail is BIND to an OFF node (CSC-1479). Reached only by BAR (CSC-1165) or SHUNT (CSC-1530), never by a sanctioned PASS. | "unattended" (G3) | **Not supported.** The thin evidence points to a cut-off, no-exit state. "Unattended" does not capture that, and may be the wrong emphasis. |
| senlihe (0041) | 7 / 7 | 2 labels. Both its tails are UNA (CSC-1136, 1193). 3 destinations. | "turning" (G3) | **Untestable**; nothing supports "turning". |
| sahalustu (0090) | 7 / 7 | 3 of its 4 coordinate-bearing uses are PASS `to`, a later pass (CSC-1296, 1352, 1498; p = 10⁻³). 3/7 on damaged objects. | none | Nothing firm. |
| arlutu (0219) | 7 / 7 | All Stratum II. Two UNA-EVERY tails (CSC-1291, 1500). Its only coordinate is `nu-rolun`, "behind" (CSC-1479). | "old" (G4) | **Untestable.** One datum could be read toward "old"; that is not evidence. |

**Overall.** None of the frequent roots shows the selectional behaviour its state gloss predicts. The "sealed" root never takes a closure; outside the top thirteen, the "barred" root ketirnu (CSC-0029) never takes BAR. That is what one expects if roots are labels of node-states whose meanings have no grammatical consequence. The Archive's G3 cap on root glosses is, if anything, generous: apart from what the bound pairs show, none of these glosses is recoverable from this corpus.

---

## C. `[41]`: what can be established

1. **It is a genuine written unit, not a copyist's artifact.** It occurs on three intact Ch-1 objects: CSC-1121 (accessioned 1886), CSC-1128 (1889) and CSC-1325 (accessioned and catalogued in 1943). CSC-1325 never passed through the nineteenth-century registers. The written occurrences also share a grammatical environment, which an artifact would not.
2. **It is a warrant.** It is always segment-final in the warrant slot and never stacks.
3. **In writing, it is a closure warrant.** All 3 written occurrences are on closure records:
   - CSC-1121: `-ar-pel` (BAR);
   - CSC-1128: `-ru-sen` (FRB);
   - CSC-1325: `-halu-sen-li` (FRB).

   The written baseline for FRB or BAR is 13/354 warranted segments (3.7%), so chance gives p ≈ 5×10⁻⁵. Two of the three also carry the closure coordinate `hilun-nu-hilun`. `[41]` and `nes` are complementary: closures take `[41]` or `hos` and never `nes`. What closes a `-sen` edge is exactly what FRB leaves unsaid, and `[41]` is the provenance mark that goes with that.
4. **In Ch-4 it is formulaic.** It ends all nine formulae, closure or not. There it follows a ritual-only unit (`lunkani`, `nisarlu`, `rosilpe`, `tuwalsi`), a position that never occurs in writing. It is said after the syllable count, outside the meter (`formulae.yaml`). Its spoken form, "forty-one", is HEL's catalogue number. So Ch-4 cannot testify to its sound, age or independence.
5. **Not established:** its sound value, its meaning, and who or what it names. The corpus supports "the warrant of closure records" and nothing beyond that.

---

## D. Stratum III: is there meaning to recover?

**Answer: there is a great deal of form, one demonstrable function, and no recoverable meaning. No reading is supportable.**

**Structure.** The 79 sequences (707 tokens) collapse into a small set of repetition templates: 20 as catalogued, 18 after two boundary adjustments. 74/79 lengths are divisible by three. The five exceptions become attested templates under the two boundary judgements the Archive itself mentions:
- the three 7-unit provisionals (CSC-1080, 1195, 1279) become ABCADC if units 2–3 are joined;
- the two 10-unit Ch-2 plates (CSC-1210, 1446) become ABCADEABC if the plate-edge final unit is dropped.

The templates fall into five families:
- **Refrain triads (44).** Triads (x, y, R) with a constant group-final refrain R: ABCBDCAEC ×13, ABCDECAFC ×10, ABCADC ×7, ABCDEC ×5, ABCBDCDECAFC ×5, and longer chains. The x/y slots behave like path notation. Each triad often opens with the previous triad's second unit, and the first unit returns to open a later triad. CSC-1052, for example, runs A→B→D→E→F→G→H and then A→I, with `kaskurhar` as R throughout: a rooted tree.
- **Mirrors (15).** ABCCBA ×7, ABCDADCBA ×5, ABCDEAAEDCBA ×2, and the 18-unit CSC-1294.
- **Hub/envelope forms (9).** ABCADEABC ×8, where A opens every triad and triads 1 and 3 are identical; ABCADEAFBACD ×1.
- **Closed cycles (5).** ABCCDEECA, i.e. (A,B,C)(C,D,E)(E,C,A).
- **Six residual forms.**

The same templates occur in Ch-1, Ch-2 ("whole record" plates) and Ch-4 (CSC-1005, CSC-1258), and never in Ch-3.

**Sound patterning.**
- Units syllabify completely into the 48-syllable code (387/387; only 2 are ambiguous).
- 84% end in a coda. Closed syllables are used near-uniformly (`lus` 41 … `nes` 15).
- Onsetless syllables are almost absent: 2 in III units, against 84 in the register's roots.
- Distinct types within a sequence share their first syllable 3.4× more than chance (8.2% vs 2.4%). This alliteration is visible in CSC-1432 (`har-` ×5), CSC-1060 (`sa-` ×4) and CSC-1498 (`kur-` ×3).
- Final-syllable agreement is at chance (2.8% vs 3.4%), so the Archive's "terminal-syllable agreement" is not borne out.
- 28/387 types (7%) contain an internal repeat or ring, against 2% of roots: `tultultul`, `yunyunyun`, `kalyunkikal`, `tirlitir`, `walyupelwal`. The ring form appears inside units as well as across sequences.

**Decipherment attempts, and why each fails.**
- **Morphological.** No III unit contains a registered root. The closed syllables inside units do not follow functional-formative frequencies: `nes`, the commonest warrant, is the rarest closed syllable in III.
- **Distributional.** 381/387 types occur in one sequence only. Six recur:
  - `tirakur` in 5 sequences: refrain in CSC-1146/CSC-1258, palindrome centre in Ch-4 CSC-1005, a node slot in CSC-1247/III and CSC-1283. So it has no fixed function.
  - `nusar` in 3.
  - the other four only in the identical pair CSC-1146 = CSC-1258.
- **Host-gloss.** A III field shares no more syllables with the functional segment it follows than chance: Jaccard 0.115 vs 0.111, permutation p = 0.33. Templates do not track the host type.
- **Graph reading.** The refrain triads, mirrors, hubs and cycles are formally homologous to chains, junctions, orientation-invariant reading and closed traces in the functional grammar. But no unit can be tied to any node or edge, so this is a structural analogy, not a reading.

**The one function that is supportable: placement.** On intact objects, a III field follows a record that says a route does not continue 34 times in 97 (35%):

| Preceding record | III field follows |
|---|---|
| kalsira-ru | 11/24 |
| SIM (shadow segments) | 5/11 |
| tail-only `-mun` | 8/23 |
| lartuki-halu | 6/19 |
| FRB | 3/8 |
| Plain positive routes | 7/57 (12%) — Fisher p = 0.002 |
| Label objects | 0/153 |

This is a checkable, within-object version of the Archive's locus-level claim that III clusters where the map shows no outbound edge. The Utterance, Instrument and Palimpsest schools can all accommodate it.

**Conclusion.** The material is systematically composed or formatted, sits at dead ends of the record, and is semantically closed. The lack of a correlate, the lack of repetition across contexts and the lack of a bilingual together leave no route to meaning.

---

## E. The one thing the Archive has most wrong

**Its damage model: the boundary between damage and grammar, drawn wrong in both directions, when its own catalogue draws it correctly.**

The catalogue's condition field and warrant slot separate damage perfectly. Every intact-object segment is warranted (320/320), and every genuine break is on a worn, fractured or eroded object (35/35). Against that:

- **The Archive files grammar as damage.**
  - 66 of its 101 "broken halves" are complete, warranted statements on intact objects: all 24 kalsira-ru (still flagged `D-BROKEN` sixty years after Keele), all 19 lartuki-halu and all 23 tail-only `-mun`.
  - Eight of the `-mun` ones are `-ken-mun`. For these the broken-half method infers a missing THRU-headed node, from a segment that says no such edge exists.
  - True damage is 8% of segments, not 24%, and not the handbook's 41%.
- **Arguments built on the inflated figure fail.**
  - The "misparsed damage" deflation of shadow segments (§5.5) does not survive: the 12 shadow segments are complete SIM→OFF pairs, 9 of them on intact objects and 11 warranted. OFF nodes take a motion head only under SIM (12/12).
  - Hallam's co-occurrence evidence also fails: `-ar` is anti-correlated with breaks.
- **The Archive files damage as grammar.** ADJ is a seventh edge class that occurs only on damaged surfaces and accounts for every ill-formedness finding in the catalogue.

The audit the handbook says "has never been run" takes one cross-tabulation. It settles Keele, Redfern and Hallam's evidence, and it removes most of the "damage" the Archive leans on.

---

## F. Method (brief)

- **Parse.** A slot parser for every segment, using transliteration and gloss line together, checked against the transliterations. Edges were paired tail→head and classified as paired, headless before a vowel, headless before a consonant, lone tail or lone head. The published figures were reproduced before anything was inferred.
- **Cross-tabulations.** Object condition × warrant presence × break type. Incidence × position, condition and source. Edge class × incidence, grade, polarity and coordinate. Warrant × grade, polarity, closure and channel, with binomial and Fisher exact tests. Polarity × `-he` × stratum and profile, and multi-polarity segments.
- **Concordances.** Full concordances for kalsira, lartuki and the thirteen frequent roots. A root×feature association screen (Fisher, p < 0.01, reported with multiple testing in mind).
- **Place tests.** Permutation tests of root–locus clustering. A same-locus label test against its exact null. BIND and LOCUS-slot inventories.
- **Stratum IV.** Slot structure, slot-1 transition constraints, slot-2 frequency comparison with Strata I–II (Spearman), and inventory gaps (`yun`, `lus`, `ka`).
- **Stratum III.**
  - Canonical repetition templates and boundary normalization.
  - Syllabification against the 48-syllable list, with syllable-class distributions.
  - Alliteration and final-syllable agreement against shuffled nulls; internal reduplication.
  - Cross-sequence recurrence; host-segment syllable overlap by permutation.
  - Placement association with host record type (Fisher).
- **Coordinates.** Pattern-by-context tables (for example `hilun-nu-hilun` against BAR, FRB and the bound pairs), and multi-edge chains for Sturge.
- **What I could not test.** Hand-copy page ends, register traditions and the junction map are not in the packet. Anything that needs a PHASE magnitude, a gazetteer or a bilingual is marked undecidable.
