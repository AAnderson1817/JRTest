# Audit of the HEL Consolidated Substrate Corpus: what the published packet supports

**Scope.** This audit reads only the published packet: the handbook (A), the Stratum III volume, `catalogue.json`, `register.json`, `figures.json` and `formulae.yaml`. Every count below was computed from `catalogue.json` with the Archive's own gloss lines used as the parse. My parse reproduces the Archive's published figures exactly: 4,016 tokens, 417 functional segments, 101 broken, 34 stacked warrants with 11 reversed, 54 SHUNT+RECUR edges, 18 ADJ halves and 0 ADJ pairs. So the numbers here are the catalogue's numbers, not a rival transcription. One limit applies throughout: the catalogue is itself HEL's transcription. Where the objects would say something different from the Standard, this packet cannot show it.

**Verdicts at a glance**

| # | Dispute | Verdict | Conf. |
|---|---|---|---|
| 1 | Onslow: SHUNT/RECUR | Undecidable. The two-class case has no support in Strata I–III beyond the Standard's spelling, and the merger has no direct support either | 0.65 |
| 2 | Hallam: `-ar` | Side 1 in the sense that matters: `-ar` is not an incompleteness or damage notice, because all of Hallam's correlations are absent or reversed. But the junction map's reading of `-ar` is not licensed either | 0.7 |
| 3 | Redfern: ADJ | Side 2. ADJ is a damage convention, not an edge class. It is not specifically nineteenth-century: it is applied to damaged objects accessioned from 1886 to 2023 | 0.9 |
| 4 | Ladder `-sen` scope | Undecidable for the plaque. Weak lean to Cardwell (edge scope) | 0.6 |
| 5 | Keele: `kalsira-ru` | Side 1 on structure: a fixed unit that never takes a node-word destination. The gloss "sanction ends here" is undecidable, and the catalogue hides where the tail leads | 0.8 |
| 6 | Sturge: anchor | Undecidable. Nothing favours Sturge; two weak observations fit the Standard | 0.75 |
| 7 | 1969 `lartuki-halu` paraphrase | Split. "No edge is claimed" is supported. "Attendance lapsed, not resumed" is unsupported and weakly contradicted | 0.65 |
| 8 | Locative vs Stative | Side 2, negatively: roots do not behave as place names | 0.75 |
| 9 | REG `nes` restyling | The restyled gloss fits better, but without "human": the evidence supports "entered without an attestor" | 0.6 |

---

## A. The disputes

### A0. Three corrections to the evidence base (used throughout)

**1. The break inventory is two populations, and only one of them is damage.** The catalogue flags 101 of 417 segments as broken (D-BROKEN), which is 24.2%. The handbook says roughly 41%. Sorted by the object's recorded condition, the 101 separate cleanly:

- **66 are on intact objects, every one with its warrant present.** These are 24 `kalsira-ru` (e.g. CSC-1061 `kalsira-ru · hos`), 19 `lartuki-halu` (e.g. CSC-1020), and 23 tails carrying IMP `-mun` (e.g. CSC-1045 `isyuhi-in-ru-mun · tir`, CSC-1047 `kasketo-in-ken-mun · hos`).
- **35 are on worn, eroded or fractured objects, and 32 of those have no warrant.** They fall on about 30 different roots (e.g. CSC-1131 `inhesi-in-ru`, CSC-1416 `istule-in-pel`, CSC-1483 `tu-kaki-in=…`).

Breaks attributable to damage are therefore **35/417 = 8.4%**. The catalogue still files all 24 `kalsira-ru` segments as `D-BROKEN, damaged, "-ru ⌀"`. **Keele's 1963 reassignment was never applied to the catalogue**, and the same error covers 42 further segments.

**2. The handbook argues its disputes with numbers its own catalogue does not contain.** `figures.json` agrees with the catalogue; the handbook's figures do not.

| Quantity | Handbook | Published figures / catalogue |
|---|---|---|
| Share of sequences ending in a broken half | ~41% | 24.2% (8.4% on damaged objects) |
| SHUNT/RECUR flagged edges | ~380 | 54 (35 excluding the frozen `lartuki-halu`) |
| Junction-map nodes; share resting on `-ar` alone | 214; ~60% | 157; 153 (97.5%) |
| ADJ-only edges | 87 | 18 |
| Stratum II head-absent environments (Ch-1; short; undetermined; older-branch head present) | 212 (148; 63; 85; 31) | 24 (13; 4; 9; 2) |
| Longest sequence; sequences over 30 units | 41; six | 25; 0 |
| Tokens in sequences of 3 or more units | ~2,900 | 4,012 |

**3. Stratum labels are mostly not formally grounded.** A segment's "profile" is assigned from four features. Stacked warrants or `-he` make it profile I; a head-absent edge, or polarity without `-he`, make it profile II. **277 of the 387 Stratum I/II entries contain no segment with any of these features**, and for those entries the filed stratum (71 I, 206 II) is not predicted by channel, source, date, condition or warrant.

Yet all 24 `kalsira-ru` records and all 19 `lartuki-halu` records are profile I/II, and all are filed as Stratum II. At the 75% base rate that would happen by chance with probability about 0.001 and 0.004 respectively. The filing follows the reading.

There are contradictions in both directions. 17 entries filed as Stratum I contain only profile-II segments. One Stratum II entry, CSC-1479, carries `-he`.

---

### 1. Onslow 1971: are SHUNT and RECUR one class split by the 1908 consolidation, or two classes?

**Verdict: undecidable from this corpus. Confidence 0.65.** The case for two classes in Strata I–III is far weaker than the handbook presents; Onslow's merger is not demonstrated either.

- **Size of the class.** RECUR has 24 edges, but 19 are the frozen `lartuki-halu`, which projects no edge even on the Archive's own frozen-pair reading. **Live RECUR is 4 complete edges plus 1 fragment:**
  - CSC-1001, the Ch-4 return formula (recited)
  - CSC-1193, a 1912 plate: `ru-halunyu-ar-halu · ha-olpele-in`
  - CSC-1325, accessioned 1943
  - CSC-1410, accessioned 1965
  - CSC-1418, accessioned 1966, fractured

  SHUNT has 30 edges: 24 complete, 4 reduced and 2 on damaged fragments. The hazard grading that depends on the distinction rests on these 5 tokens, not on about 380.
- **Aubrey's defence (2007) is contradicted by the catalogue.** RECUR never sits on a MED node: its tails are TERM (21), JCT (1) or unmarked (2), and all its heads are TERM. SHUNT, by contrast, has 7 MED tails (e.g. CSC-1095 `ru-lusluru-is-tul · tu-munkaru-is-tul-nir`, CSC-1470 `ru-kalkurpu-is-tul`).
- **Vance's complementary distribution (2004) is uninformative.** It holds only if `lartuki-halu` is excluded, since CSC-1253 bears `harhape-in-tul · tu-lartuki-in-halu`. And with 5 live RECUR objects against about 27 SHUNT objects in about 380 functional objects, chance predicts about 0.3 co-occurrences. Observing none is what one class split in two would also produce.
- **The only real contrasts are in Stratum IV.** CSC-1522 (`hoslustu tul nirwaltel · pelkal halu senhitel`) and CSC-1526 (`tirtilun tul nihitel · sartir halu rusensenra`) place `tul` and `halu` in the same middle slot of IV's rigid triads. But that slot takes any formative, including UNV `lus` and PREP `ka`, which are never attested in Strata I–II. So IV's testimony about I–III classes does depend on the Palimpsest question, as the handbook says.
- **Onslow's mechanism.** The catalogue records register tradition for only 20 entries, and none carries a SHUNT or RECUR edge. It does confirm Onslow's premise that the traditions cut the arrival flick differently: on CSC-1124 (`arhalu`) and CSC-1147 (`arpepu`) the older branch hand cuts a head half that the Standard omits. It does not confirm the premise for these two classes. The mechanism's one indirect prediction is that both transcriptions coexist in the pre-1908 consolidated layer. That is not met: pre-1908 `-halu` occurs only inside `lartuki-halu` (CSC-1119, 1142, 1178, plus the undated 1020 and 1030), and every `ha-` head is post-1908 or recited. With 5 tokens, though, zero pre-1908 cases has a chance probability of about 0.3, so this proves nothing.
- **No duplicate records.** No pair of records shows a `tul`/`halu` alternation over the same content. The only duplicated root sequences are `kenutulti → kalsira-ru` (CSC-1432, 1459) and `harnuli → kurhali` (CSC-1165, 1530).

### 2. Hallam 1976: does `-ar` mark a junction, or that the record stops here?

**Verdict: side 1 on the evidence, qualified. Confidence 0.7.** `-ar` is not an incompleteness or damage notice: every correlation Hallam assembled is absent or reversed in the catalogue. But the junction map's use of `-ar` is not licensed by the corpus either.

There are 154 `-ar` tokens, all in Ch-1 and Ch-2 and none in Ch-4.

- **Damage (reversed).** `-ar` makes up 27% of node words on intact objects, 22% on worn, 12% on fractured and 5% on eroded ones. In genuinely damaged segments it is 11/94 (12%), against 143/461 (31%) in clean segments (Fisher p ≈ 7×10⁻⁵). In the 101 broken-flagged segments it is 5/137 (4%).
- **Margins (reversed).** Within multi-word chains, `-ar` is 6/182 first words and 9/182 last words, but 16/49 medial words (p ≈ 10⁻⁸). The medial `-ar` nodes carry both a head and a tail, and the record continues through them (CSC-1065 `ru-yunpuru-ar-ru · ru-pusarsi-in`; CSC-1200 `ru-tulnuli-ar-ru · ru-silipelka-ar-tul · tu-toyunli-in`). For these, "this record does not continue" is false.
- **Hand copies (not supported).** `-ar` is 2 of 23 node words in the 15 pre-photographic hand copies: CSC-1108 (medial) and CSC-1112 (a label). It never ends a multi-word copy. The catalogue does not record page ends, so the page-end claim itself cannot be tested, but `-ar` is not characteristic of hand copies.
- **The 1979 reply is accurate but rests on labels, as Hallam said.** 101 intact Ch-1 entries bear `-ar`, and **93 of them bear it only in single-word label segments**. 123 of the 154 `-ar` tokens are single-word segments. On labels, incidence tracks the medium: `-ar` is 76–92% of Ch-1 object labels, about 40% of Ch-2 plate labels and 1/9 of hand-copy labels (object vs hand copy p ≈ 0.01).
- **The qualification.** 97.5% of the junction map (153/157 nodes) rests on `-ar` alone, mostly on labels. On a label, the Standard's "other edges attach here, not stated" and Hallam's "the rest is not given here" differ only by an existence claim that no record can check. And even the Standard's gloss never implies a fork, which is what a junction is. So the map's nodes are not known junctions under either reading. That is Hallam's operational point, reached without her evidence.

### 3. Redfern 1993: is ADJ an edge class, or a nineteenth-century damage convention?

**Verdict: side 2, a damage convention, with the date wrong. Confidence 0.9.**

- **Condition.** There are 18 `-yun` tails on 15 entries. **All 18 are on worn (7), eroded (6) or fractured (5) objects; none is on an intact object.** The baseline is that 81% of Ch-1/Ch-2 entries with segments are intact (307/378), so the chance of all 15 entries being non-intact is about 10⁻¹¹. All are Ch-1 objects; there are none on plates or hand copies.
- **Ill-formedness.** **Every one of the catalogue's 11 ill-formedness findings (8 E-CARRIER, 3 E-OFF) falls on the word immediately after a `-yun`.** Examples: CSC-1054 `situ-in-yun · isnihe-in=hostuhe-hilun-pukal`; CSC-1552 `yuhosli-in-yun · arpepu-in=hilun-nu-pukal`; CSC-1049 `kasketo-in-yun · kurhali-ol`; CSC-1362 `walpu-in-yun · olkini-ol`.
- **The head half was there.** Eight of the 18 following words carry a coordinate, and only a head-bearing word may carry one. So those words had a head half that is now lost. Read `-yun` as "an edge stood here and both flicks are illegible" and all 11 violations disappear. The handbook's "100% of coordinate carriers are head-bearing" (§4.3) then holds without exception. As catalogued it is 107 of 115, with the 8 exceptions all after `-yun`.
- **Date.** Redfern's origin story is not borne out. Six tails are on objects accessioned 1886–1903, nine on objects accessioned 1939–2023 (the latest is CSC-1552, 2023), and three are undated. There are none in the branch-register hand copies. This is a damage notation the Standard's transcribers still apply to incised objects, not a nineteenth-century relic.
- **The shape defence proves nothing.** Every string in the corpus is built from the 48-syllable list, so a damage mark conforming to morpheme shape is guaranteed.
- **Consequence.** The handbook's "87 ADJ-only edges" are 18 in the catalogue, and none of them is an edge.

### 4. The Ladder plaque: is `-sen` segment-scoped (Long Reading) or edge-scoped (Cardwell)?

**Verdict: undecidable for the plaque. Weak lean to Cardwell (edge scope). Confidence 0.6.**

The plaque is CSC-1165 (L-7, accessioned 1904): `harnuli-ar-pel-sen · pe-kurhali-in=hilun-nu-hilun · hos`.

- **No Stratum I parallel of the needed kind can exist.** The scope clitic `-he` has 7 tokens (CSC-1352, 1289, 1313, 1339, 1173 twice, 1479), and **all are on PASS or THRU edges**. It never occurs on BAR, SHUNT or RECUR, and never with IMP. BAR with polarity occurs only twice in the whole corpus, on the plaque and in the Ch-4 sealing (CSC-1012), and neither has `-he`. There is no evidence that a BAR edge ever took `-he`.
- **The "Stratum II lost `-he`" premise is partly made by classification.** It is true of segment profiles because polarity without `-he` is one of the things that makes a segment profile II. At the level of filed entries it fails:
  - Stratum I entries carry polarity without `-he` on complete edges: CSC-1149 `helusyu-in-tul-nir`, CSC-1176 `olsitu-in-ru-ti-nir-kur`, and **CSC-1200 `lunkinu-in-tul-sen`, a `-sen`**. There are also 12 `-mun` tails in Stratum I entries.
  - Stratum II entry CSC-1479 has `-he`.
- **Where `-he`-less polarity can be tested, it is edge-scoped.** CSC-1328 (`sinisensa-in-ru-nir-kur · arhiha-ar-tul-sen-kur · tu-harhale-ar`) and CSC-1337 (`hoskalnu-in-ru-nir · arhisa-is-ru-sen · … · ru-munluhape-is-ru-nir`) carry UNA ("not closed") and FRB ("closed") on different edges of one segment. Under segment scope, each of those segments would contradict itself. Segment-scoped polarity is demonstrated nowhere in the corpus. That is the whole of the lean.
- **The Long Reading's best support is outside the written corpus.** The Ch-4 sealing (CSC-1012, `nirtoka-pel-sen · pe-olsihe-in=hilun-nu-hilun`) has the plaque's exact structure and is "said when a locus is placed under containment". But Ch-4 is HEL's own channel and that use is HEL's.
- **Hallam's dissolution fails on her own evidence** (dispute 2), so the junction premise stands, but only at the Standard's weak grade.
- **The only other `harnuli → kurhali` record** is CSC-1530, a 2014 Ch-2 plate: SHUNT, no closure. It cannot be used, because roots do not identify nodes (dispute 8).

### 5. Keele 1963: is `kalsira-ru` a frozen pair or a literal onward PASS edge?

**Verdict: side 1 on structure. Confidence 0.8.** It is a fixed unit whose tail never takes a node-word destination. The literal reading, an onward PASS edge whose head was lost, is refuted. The gloss "the sanction ends here" cannot be decided.

- **Distribution.** There are 27 tokens: 24 bare `kalsira-ru` (18 Ch-1, 6 Ch-2 plates) and 3 completed `kalsira-in-ru` in Stratum I (CSC-1407, 1448, 1460). All 24 bare forms are on intact objects, all have their warrant, and **0 of 24 is ever followed by a node word**.
- **It is a different form, not a damaged one.** **The 24 bare forms are the only node words in Ch-1 and Ch-2 without an incidence marker.** Every other written node word carries `-in`, `-is`, `-ar` or `-ol`, and every compositional `kalsira` has `-in` (CSC-1065, 1191, 1407, 1448, 1460). `kalsira-ru` is therefore not `kalsira-in-ru` with a lost head.
- **Damage does not select a root.** The 35 genuinely damaged dangling tails fall on about 30 roots. The intact dangling tails concentrate on `kalsira` (24) and `lartuki` (19), or on a single polarity (`-mun`, 23).
- **Weak points in Keele's published case:**
  - "No object carrying one carries any other break" is trivially true: every `kalsira-ru` object has exactly one functional segment.
  - "At segment interiors as often as margins": in the catalogue all 24 are segment-final, immediately before the warrant.
  - The three compositional Stratum I tokens, on which the lexicalization-as-change argument (§10.1) depends, were all **accessioned after the 1963 review** (1964, 1980, 1985).
  - The Stratum II filing of all 24 has no formal basis (A0.3).
- **What the frozen reading leaves out.** On **11 of the 24 objects (11 of 18 in Ch-1) the incised field continues after the warrant into a Stratum III field**: CSC-1038, 1061, 1153, 1158, 1160, 1247, 1360, 1408, 1432, 1472, 1510. For Ch-1 objects ending in an ordinary chain the rate is 19% (overall 11%, p ≈ 3×10⁻⁴). The handbook's "nothing is required to follow, and in Strata II–III nothing ever does" is true only because what follows was filed as another stratum. None of those fields begins with `ru-`, so this is not a mis-cut head. But whether the tail points into that material or closes the functional record before it, the corpus cannot say.
- **The only locus-bound form.** `kalsira-ru` is the only root that recurs at a find locus. Every functional record from L-16 is `kalsira-ru` (CSC-1068, 1287 "Quiet Sixteen", 1459), and so is every functional record from L-14 (CSC-1038, 1510). Across the corpus it occurs at 22 loci.

### 6. Sturge 1958: is a coordinate on a multi-edge chain measured from the immediately preceding tail-bearer, or from the chain-initial node?

**Verdict: undecidable. Confidence 0.75.** No magnitude exists anywhere in the corpus. Nothing favours Sturge, and two weak observations fit the Standard.

- **How many cases.** The Archive counts 12 multi-edge coordinate segments; counting reduced and ADJ edges gives 17 (e.g. CSC-1191, 1289, 1299, 1337, 1470).
- **Coordinates respond to the immediately preceding edge.** Every single-edge BIND coordinate is `sa-kihar` (CSC-1002, 1008, 1040, 1169, 1471; CSC-1122 has its PASS slot lost). But no multi-edge chain ends in BIND, so this cannot discriminate between the readings.
- **One token fits the Standard.** Single-edge SHUNT coordinates are never `kihar` (0 of 8). CSC-1299 (`lukaski-in-tul-kas-sar · tu-yunpuru-ar-ru-ti · ru-kenpe-ar=hilun-sa-kihar`) is SHUNT followed by PASS, ending in `kihar`. That is natural measured across the last PASS leg (the Standard). It is awkward measured from `lukaski` across a displacing SHUNT leg (Sturge).
- **No accumulation with chain length.** `kihar` is 20% of single-edge coordinates and 27% of multi-edge ones; displaced values are 44% and 47% (n = 59 and 15). Sturge does not strictly require accumulation, so this is weak.
- **The catalogue's findings cannot serve as evidence.** They already encode the Standard: the D-ANCHOR finding ("the anchor word is missing") on CSC-1296, 1340, 1418, 1423 and 1483 assumes it.

### 7. The 1969 `lartuki-halu` paraphrase: right or wrong?

**Verdict: split. Confidence 0.65.** "No edge is claimed" is supported. "The attendance-state lapsed and was not resumed" is unsupported and weakly contradicted. Net: not shown right, and the content cannot be decided.

- **It is a single template.** All 19 occurrences have the form `X-in-{ru|ke|tu} · {ru|ke|tu}-lartuki-in-halu=hilun-nu-hilun · {tir|nes}`. They come from 19 loci with 19 different origin roots. The arriving edge is PASS 15 times, THRU 3 and SHUNT 1.
  - The coordinate is identical in all 19; `hilun-nu-hilun` occurs on only 6 of 87 (7%) other head-bearing carriers.
  - Warrants are `tir` 12, `nes` 7.
  - All are on intact objects, and all are filed Stratum II while being profile I/II.
- **Supported: no edge.** No head appears in any of the 19, and every one is intact and warranted.
- **"Attendance" is imported from HEL's own ritual.** `lartuki` occurs nowhere else except the Ch-4 custodial formula (CSC-1002 `si-lartuki-ol`), whose use, "said over a ward at a change of custody", is HEL's.
- **"Lapsed" has its own exponent, and it is absent here.** The Archive's own gloss lines assign `-sar` LAPSED, with 8 tokens (e.g. CSC-1065 `kalsira-in-tul-kas-sar`, CSC-1345 `kihekurhe-in-ru-kas-sar`). None of the 19 carries it.
- **"Not resumed" has no correlate.** It inverts RECUR and matches nothing in the distribution. The compositional alternative fits the data just as well: a recurrence departs from a node reached on another pass, destination unstated. Once intact dangling tails are admitted, as they are for `kalsira-ru`, the "cost" the handbook assigns to that reading (19 broken segments) vanishes.
- **Stratum III follows 6 of 19** (CSC-1030, 1178, 1185, 1244, 1473, 1475).

### 8. Locative vs Stative: do the roots name places, or states of nodes?

**Verdict: side 2, negatively established. Confidence 0.75.** Roots do not behave as place names. Nothing positively shows that they name states.

- **Recurrent roots do not repeat a locus.** 72 roots appear in 3 or more functional records, averaging 4.8 records at 4.7 distinct loci. **68 of the 72 never repeat a locus.**
- **Records at the same locus barely share roots.** Same-locus pairs share a root 8 times in 284 (2.8%); different-locus pairs, 1.7% of the time. Four of those 8 same-locus shares are `kalsira-ru` (L-14, L-16).
- **The in-situ test.** Ch-2 standing patterns are photographed or copied where they stand, so they cannot have migrated. **0 of 44 same-locus Ch-2 pairs share a root.**
- **Labels.** 38 loci have two or more single-node label records, and **at none do the labels agree**. 26 label roots appear at two or more loci; `kastuhe` appears at 5 (L-97, 102, 140, 251, 276) and `kihetirlu` at 5.
- **Even the frequent roots scatter.** `kalsira` has 29 tokens at 26 loci, including Ch-2 plates at 6 loci. `harnuli`, which the register notes as "designates one node", has 7 records at 6 loci.
- **Caveat.** This refutes place-naming only on the assumption that records found at a locus sometimes speak of it, which is most plausible for in-situ Ch-2 records and for labels.

### 9. The 1949 restyling of REG (`nes`): which gloss fits better?

**Verdict: the restyled gloss, weakly, and without "human". Confidence 0.6.**

- **`nes` is the commonest single warrant**: 115 of 320 (36%).
- **It never stacks.** The 34 stacked warrants are `lekur hos` (19), `hos lekur` (11) and `tir lekur` (4). **`nes` appears in none of them**, and neither does `wal` ("no source carried") or `[41]`. So `nes` patterns with the absence value, not with the positive attestations. A positive agentive source, "registered by the system itself", could naturally be qualified as recurrent or inferred; `nes` never is.
- **Other exclusions.** `nes` never co-occurs with AUTH (the two warranted AUTH segments, CSC-1097 and 1410, both take `tir`). The 12 shadow (SIM→OFF) segments take `nes` 6 times, `hos` 5 and `tir` never.
- **Against "human".** Nothing ties `nes` to human presence. Its share is 34% on records that were the first recovery at their locus and 36% at loci already visited. The only "human" effect is in HEL's copying: `nes` appears 1 time in 13 in hand copies against 26 in 79 on Ch-2 plates.
- **So** the corpus supports an absence-of-attestation value. It supplies no registrar, against the old gloss, and no human, against the new gloss's wording.

---

## B. Roots

Frequencies in Strata I–II are flat after the top two, with a seven-way tie at rank 7, so "the ten most frequent" cannot be chosen without an arbitrary tie-break. I cover all 13. General findings first:

- **No root tracks a find locus** (dispute 8).
- **No root has a distributional correlate strong enough to ground a semantic gloss.** The only robust regularities are positional or formulaic.
- **The Archive's glossing does not follow the corpus.** Six of these 13 roots have no gloss at all. Of the register's 40 glossed roots, **8 never occur in the catalogue** (`kentuli`, `rasilke`, `sihoslu`, `munhilu`, `tokalhi`, `nukenra`, `puhosle`, `keharsi`) and **5 occur only in HEL's own Ch-4 formulae** (`lankiro`, `kanirlu`, `nirtoka`, `lunpeki`, `yuntiha`).
- Tokens here include Ch-4 and LOCUS-slot uses; counting Ch-1/Ch-2 only, `harnuli` drops to 5.

| Root (CSC) | Tokens / loci | What the evidence shows | Archive gloss | Assessment |
|---|---|---|---|---|
| `kalsira` (0012) | 29 / 26 | 24 are the frozen, incidence-less `kalsira-ru`; 11 of those objects continue into Stratum III; locus-bound at L-14 and L-16. Compositionally it originates sanctioned PASS edges (CSC-1407, 1448, 1460), a SHUNT (CSC-1065) and is once a destination (CSC-1191). Never with any polarity or BAR | "sealed" G3 | **Partly right at best.** Fits the frozen form's terminal role, but is contradicted by the compositional tokens, where a "sealed" node originates sanctioned onward edges. It reads as the pair's gloss, not the root's |
| `lartuki` (0077) | 20 / 20 | 19 are a single formula slot (`lartuki-halu`); 1 is in the Ch-4 custodial formula | "attendance" G3 | **Unfounded.** Imported from HEL's ritual use |
| `arhesi` (0038) | 12 / 12 | Vowel-initial; never bears a head half (0/12), even as a destination (after `-yun` in CSC-1124, 1341; reduced in CSC-1132). 5 JCT. Once with `[41]` (CSC-1128) | "common" G3 | **Unfounded.** Its only regularity is the Standard's vowel-initial head environment |
| `kastuhe` (0039) | 8 / 8 | 5 labels, 4 of them `-ar`; label root at 5 loci | none | Nothing to assess; no correlate |
| `silipelka` (0076) | 8 (+1 LOCUS) / 9 | 4 labels; once fills a LOCUS slot (CSC-1193 `=silipelka-sa-hilun`) | none | Nothing to assess |
| `kihetirlu` (0079) | 8 (+1 LOCUS) / 9 | `-ar` 5/8 (base 24%), label-heavy; once in a LOCUS slot (CSC-1536) | none | Nothing to assess |
| `harnuli` (0007) | 7 / 6 | **Never a destination (0/7 heads)**: always chain-initial or a label. In the departure formula and the long word (CSC-1010, 1003), the Ladder, Example 1 (CSC-1191) and CSC-1530 | "in standing" G3; register notes "designates one node" | **Unfounded.** "One node" is contradicted by 6 loci. The origin-only position is real but small |
| `yunpuru` (0011) | 7 / 6 | SIM grade 3/7 (CSC-1033, 1172, 1299) against a 3% base | none | A weak SIM association; nothing semantic |
| `arhisa` (0021) | 7 / 7 | Vowel-initial, head-less, label-heavy | none | Nothing to assess |
| `kurhali` (0104) | 7 / 7 | 4 of 7 on edges that do not go through: IMP twice (CSC-1223, 1388), BAR head (the Ladder), SHUNT head (CSC-1530). Base about 10% | "unattended" G3 | **Unfounded.** Derived as the opposite of "attendance". The data point, weakly, to non-traversal, which the gloss does not capture |
| `senlihe` (0041) | 7 / 7 | UNA 2/7 (CSC-1136, 1193); twice in SIM segments (CSC-1172, 1314) | "turning" G3 | **Unfounded.** Note that `[41]`'s bracket number collides with this register entry |
| `sahalustu` (0090) | 7 / 7 | Carries a coordinate 4/7 (base 18%); a destination of PASS and SHUNT | none | Nothing to assess |
| `arlutu` (0219) | 7 / 7 | Vowel-initial; UNA 2/7 (CSC-1291, 1500) | "old" G4 | **Unfounded**; the register itself marks it as one analyst's |

None of the Archive's glosses for these roots can be called right. One is partly consistent with the evidence (`kalsira`). The rest are unfounded rather than refuted: the corpus lacks the correlates that could refute them. The "2 of 7" associations above are weak once one allows for the many comparisons made.

---

## C. `[41]`: what can be established

1. **Distribution.** There are 12 tokens: all 9 Ch-4 formulae, and **3 intact Ch-1 objects**: CSC-1121 (accessioned 1886, L-311), CSC-1128 (1889, L-350) and CSC-1325 (1943, L-140). Because the Ch-1 instances are on objects, none can be a hand-copyist's artifact. What remains open is whether the Standard's transcription of those objects is sound.
2. **It is a warrant-slot filler, not a separate category.** It always sits in the segment-final warrant position and **never co-occurs with any of the five warrants** (0/12). Like `nes` and `wal`, it never stacks.
3. **On objects it goes with closure.** **All three Ch-1 segments carry a closure**:
   - CSC-1121: BAR (`tiluyunhe-ar-pel · pe-pelra-in=hilun-nu-hilun`)
   - CSC-1128: FRB (`arhesi-in-ru-sen · ru-telnuro-in`)
   - CSC-1325: FRB (`larluki-in-halu-sen-li · ha-munkaru-in=hilun-nu-hilun`)

   Only 14 of 303 other Ch-1 segments (4.6%) have FRB or BAR, so three of three is unlikely by chance (p ≈ 10⁻⁴). Two of the three also have the coordinate `hilun-nu-hilun`, as does the Ch-4 sealing, the only Ch-4 formula with BAR+FRB.
4. **The Ch-4 attestations are not independent evidence.** Crews say "forty-one", a catalogue label, in that position. The ubiquity of `[41]` in the recited formulae therefore cannot be separated from HEL's cataloguing.
5. **Book-keeping.** `[41]` has no entry in `register.json`, and **its bracket number collides with CSC-0041, which the register assigns to `senlihe`**.

**Not establishable:** a sound value, a meaning, or whether it is a warrant semantically rather than just positionally. The defensible description is: a written-channel warrant-slot value, exclusive of the other warrants, found on objects only with barred or closed edges.

---

## D. Stratum III

**Is there meaning to recover?** No semantic reading is supportable from this corpus. **Structure, however, is real, and more of it can be recovered than the Archive reports.**

1. **Repetition templates.** Reduce each sequence to its pattern of repeats and the 79 sequences collapse into **20 templates**, with **the top nine covering 60**. The main families are:
   - Refrain every third unit (41 sequences), e.g. ABCBDCAEC in 13 sequences and ABCDECAFC in 10, the latter including CSC-1146 and 1032.
   - Mirrors (15), e.g. ABCCBA and the palindrome ABCDADCBA (CSC-1027, 1033/III, 1231/III, 1419, 1448/III).
   - First triad returns at the end (6).

   These templates are shared across 31 loci, three channels and accession dates from 1874 to 2025. The vocabulary almost never repeats across records (381 of 387 types occur in one sequence; recurrence within a record 0.58, elsewhere 0.04). The *form* does. This is cross-record repetition, which §3.3 says is lacking.
2. **The exceptions to divisibility by three are systematic.** The three 7-unit Ch-1 sequences (CSC-1080, 1195, 1279) share one template, ABCDAED. Merging units 2 and 3 in each, the "contested boundary", turns all three into ABCADC, a template four other sequences already use. The two 10-unit Ch-2 plates (CSC-1210, 1446) share ABCADEABCA: the first-triad-returns template plus one closing return. So all 79 sequences fit a template family.
3. **The null parse survives resegmentation.** Rebuilding units from registered roots plus any formatives, only 7 of 387 types parse as node words, against 1.6% for random strings from the syllable list. Stratum III is not misparsed Stratum I in bulk.
4. **Stratum III is in contact with the functional grammar.** Of the 41 fields that follow a completed segment, **30 follow a segment whose stated path never arrives on-path**:
   - `kalsira-ru`: 11 of 24
   - `lartuki-halu`: 6 of 19
   - IMP `-mun` tails: 8 of 23
   - SIM→OFF shadow segments: 5 of 12

   That is 30/78 (38%), against 11 of 100 (11%) after ordinary chains and 0 of 176 after labels (p ≈ 2.5×10⁻⁵). The claim of "no attested contact" is true only unit by unit. The filing boundary, drawn at the warrant, hides a dependency on the preceding construction.

**Is the class an artifact of filing? Partly: its boundary and several of its signature facts are; its internal structure is not.**

- **The partition** (zero contact at the unit level) restates the sorting rule, as the handbook concedes.
- **The "silhouette"** is made by the Standard.
  - The 85% coda-final share comes from the rule that forces roots, and only roots, to be vowel-final.
  - 38 of the 48 list syllables are homographs of functional formatives, so the 72% "formative-like" syllable content of Stratum III is at chance.
  - That 386 of 387 types share a first syllable is forced by pigeonhole: 387 types, at most 48 first syllables. The comparison with functional units is also false: 290 of the 294 attested functional root types share a first syllable too; only the 35-root commanded core obeys the distinctness rule.
  - Terminal-syllable agreement within triads is rare: 10 of 127 triads.
- **The Ch-4 members add little independent weight.** CSC-1258 (Sowerby) and CSC-1146 are one text. Both Ch-4 sequences contain `tirakur`, which is also in CSC-1247/III (accessioned 1928, before Sowerby) and CSC-1283.
- **The junk-drawer version of Palimpsest is contradicted.** Accession bias cannot produce a small set of repetition templates shared across 150 years of recoveries. What survives of Palimpsest is its "not semiotic at all" branch: refrain-at-thirds and mirror symmetry are also what a periodic or symmetric physical process would leave.

---

## E. The one thing the Archive has most wrong

**It draws the line between damage and morphology with its parser instead of with the objects, and it gets the line wrong in both directions.**

- **Damage promoted to morphology.** ADJ `-yun` is treated as an edge class. All 18 instances are on damaged objects, and all 11 ill-formedness findings follow them.
- **Morphology filed as damage.** 66 of the 101 "broken" segments are intact, warranted, patterned tail forms (`kalsira-ru`, `lartuki-halu`, IMP tails). They are still catalogued as damage, 63 years after Keele corrected 24 of them.

The headline figure built on this error, "roughly 41% of sequences terminate in a broken half", is the handbook's all-purpose solvent. Measured against object condition, damage accounts for 8.4%. Several of the Archive's positions rest on the wrong line:

- **Shadow segments.** §5.5 and §12 row 16 explain them away as misparsed damage. In the catalogue all 12 keep their head-bearing OFF node (11 overtly, one in the vowel-initial environment), 9 are on intact objects and 11 have their warrant.
- **Keele's story.** The claim that `kalsira-ru` was "invisible among 41%" of breaks depends on the inflated figure.
- **The "100% head-bearing carrier" rule** is maintained by filing the 8 counterexamples as ill-formed.
- **Stratum III's non-contact.** Its fields cluster exactly after the misfiled dangling tails.

The runner-up is the same fault in another place: Stratum I/II labels that are mostly not formal (A0.3), and that follow the Archive's readings back into the arguments meant to test them.

---

## F. Method (brief)

- **Parsing.** Each segment was parsed from the Archive's gloss lines: edge halves, incidence, grade, polarity, the undocumented post-polarity formatives, `-he`, and coordinates attached to their carriers. The parse was checked against every count in `figures.json`, all of which it reproduces.
  - The undocumented formatives are `-lun` STANDING?, `-sar` LAPSED, `-ro` SPENT, `-kur` EVERY, `-li` ONCE and `-lar` UNENT?.
  - They account exactly for the figures file's "imports": H1 = 29 (STANDING, LAPSED, SPENT), H2 = 2 (UNENT), H3 = 13 (EVERY, ONCE).
  - The handbook never grades them.
- **Edges.** A tail followed by a matching head is *complete*; followed by a head-less word, *reduced*; on the final word, *dangling*; a head on the first word, *broken head*.
- **Cross-tabulations.** Every feature was cross-tabulated against channel, source (object, plate, hand copy), accession year (before or after 1908), condition, filed stratum against segment profile, position in segment, find locus, and the presence of a following Stratum III field. Tests were two-sided Fisher exact or binomial tails.
- **Specific tests.**
  - Root sharing between record pairs at the same versus different loci, with Ch-2 and labels separately.
  - Warrant co-occurrence and stacking.
  - Whether a record was the first recovery at its locus, as a proxy for human presence.
  - PHASE value against chain length and last edge class.
  - Stratum III repeat templates.
  - Resegmentation of Stratum III units against registered roots, with a random-string control.
  - A search for duplicate root sequences.
- **Caveats.** All counts are of HEL's units in HEL's transcription. Many cells are small (5 live RECUR tokens, 12–17 multi-edge coordinates, 7 `-he`, 3 Ch-1 `[41]`), and I have tried to state confidence at the grade those cells can bear. Scripts and intermediate files are in `trial/work-auditor/`.
