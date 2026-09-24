# Report: signals/protocol engineer, blind decipherment trial

**Sources.** I read only the six packet files. Every count below comes from my own parse of `catalogue.json` unless it is cited to `figures.json`, `register.json` or a handbook section. The scripts are in `work-engineer/`.

**Stance.** I treated each segment as a record with fixed-order fields. I cross-tabulated every marker against the metadata the Archive publishes but does not use as a control: condition, accession year, catalogue year, source, channel and find-locus.

## Verdicts at a glance

| # | Dispute | Verdict | Conf. |
|---|---|---|---|
| 1 | Onslow: SHUNT/RECUR | **Side 2: two classes.** Onslow's mechanism cannot produce the post-1908 RECUR tokens, and the "complementary distribution" argument is statistically empty | 0.65 |
| 2 | Hallam: `-ar` | **Side 1: a structural, junction-type marker.** Every test Hallam proposed comes out the other way. The claim that the unstated edges exist is still unverified | 0.75 |
| 3 | Redfern: ADJ | **Side 2: a damage convention, not an edge class.** Correction: it is HEL's *current* transcription convention, not only a 19th-century one | 0.9 |
| 4 | Ladder: `-sen` scope | **Leans side 2 (edge-scoped, Cardwell).** The plaque itself cannot be settled | 0.6 |
| 5 | Keele: `kalsira-ru` | **Side 1: a frozen pair that projects no edge** | 0.85 |
| 6 | Sturge: anchor | **Undecidable from this corpus** (two proxies point opposite ways) | 0.75 that it is undecidable |
| 7 | 1969 `lartuki-halu` paraphrase | **Split.** Its structural claims are right. "Lapsed" has no support, and "no edge is claimed" is misleading | 0.8 / 0.5 |
| 8 | Locative vs Stative | **Side 2: roots are not place or node designators** (whether they are "states" specifically is not shown) | 0.7 |
| 9 | REG (`nes`) | **Leans side 1: "registered by the system itself" fits better** | 0.6 |

---

## A. The disputes

### A0. Preliminary: what the instrument logs (Ch-3, Stratum IV) share with the rest

Several verdicts lean on this, so I state it once.

- **Format.** There are 64 logs, all intact, dated 1921–2025. Every log length is divisible by 3 (6, 9, 12 or 15). Each log is a strict run of **(key, value, tail) triples**, and the three positions use disjoint vocabularies:
  - 6 keys: silkalus 40, hoslustu 38, pelkal 38, tirtilun 33, raken 32, sartir 24.
  - 30 values.
  - 35 tail units.

  This framing is the "sequencing constraint the others violate".
- **The 30 values are the shared ~30 units.** 28 are functional formatives and 2 are roots (kasluhi ×7, rukalti ×1). The formatives form *complete* paradigms:
  - incidence 4/4, grade 4/4, polarity 4/4, PASS 3/3, PHASE 4/4, and the gap marker `hilun`;
  - 6 of the 7 edge classes;
  - only 2 of the 5 warrants (`nes`, `tir`).
- **Missing from Ch-3:** `yun` (ADJ), `-he`, every "import" formative (`lun/sar/ro`, `kur/li`, `lar`), `hos`, `lekur`, `wal`, `[41]`, and all head halves.
- **Found only in Ch-3:** `ka` (PREP) and `lus` (UNV). Both are cells in the Archive's paradigm tables, and neither is attested even once in Strata I–III.
- **No typing, no hidden quantity.**
  - Keys do not type their values: every key takes values from every paradigm.
  - The tail unit is not a check field. The same (key, value) pair recurs 49 times with different tails.
  - I found no sign that tails carry a magnitude.
- **Not a re-encoding of I–II.** Value frequencies do not match I–II: for example `in` is 2% of Ch-3 values but the commonest formative in I–II.
- **Reading.** Ch-3 is a fixed-frame log whose alphabet is the functional code-book. The syllables are HEL's, so the shared alphabet alone does not settle the Palimpsest question. But an arbitrary assignment would not produce a set that is closed under every core paradigm yet lacks exactly ADJ and the derived warrants.

### A1. Onslow 1971: are SHUNT and RECUR one class or two?

**Verdict: side 2, two classes. Confidence 0.65.**

- **Inventory.**
  - SHUNT: 29 tails and 25 heads.
  - RECUR: 23 tails, but **19 of them are the frozen `lartuki-in-halu`** (A7). Genuine RECUR edges are only CSC-1001 (the return formula), CSC-1193 (1912), CSC-1325 (1943) and CSC-1410 (1965), plus a head-only fragment, CSC-1418 (1966).
  - `figures.json` counts 54 SHUNT/RECUR edges. The handbook says "about 380".
- **The complementary-distribution argument carries almost no weight.**
  - SHUNT occurs on 27 of 387 functional objects (7%).
  - With 5 genuine-RECUR objects, about 0.35 of them would be expected to carry SHUNT as well. Finding none is what chance predicts (P ≈ 0.7).
  - The one object bearing both, CSC-1253, pairs SHUNT with the frozen `lartuki-halu`.
- **Aubrey's defence fails on this catalogue.**
  - RECUR tails never sit on MED (`-is`) nodes: 0 of the 4 genuine ones, and all 19 `lartuki` tokens are TERM.
  - SHUNT tails sit on TERM 18, MED 7, JCT 4.
  - So there is no skew for either side to explain.
- **Onslow's mechanism cannot produce the data.** He says the split arose when the 1908 consolidation merged pre-1908 branch registers. But the RECUR tokens on CSC-1193, -1325, -1410 and -1418 were accessioned and catalogued in the same year (1912–1966), directly under the unified Standard. So were 14 of the 19 `lartuki-halu` tokens. To keep the merger, a defender needs a new assumption: that the two branch cutting habits survived in post-1908 transcribers.
- **Stratum IV keeps them apart.** Ch-3 has `tul` (12) and `halu` (5) as distinct values in the same slot, including two near-minimal pairs that share the tail unit:
  - CSC-1335 `hoslustu tul rusensenra` vs CSC-1526 `sartir halu rusensenra`;
  - CSC-1373 `sartir tul senhitel` vs CSC-1522 `pelkal halu senhitel`.
- **Weak semantic fit.** PHASE `nikur` ("displaced, unmeasured") occurs on 3 of 11 SHUNT coordinates and on 0 of 4 RECUR coordinates.
- **Caveat.** Outside the frozen pair RECUR is so rare that its gloss is untested. Any risk table built on "about 380 flagged edges" needs recounting: the catalogue has 54.

### A2. Hallam 1976: does `-ar` mark a junction, or that the record stops?

**Verdict: side 1. `-ar` behaves as a structural (junction-type) marker, and Hallam's "record stops here" reading is contradicted wherever it can be tested. Confidence 0.75.** What stays unverified is the positive content that other edges exist.

- **Where it occurs.** 154 tokens on 148 objects. 123 are one-word label segments (`X-ar · warrant`, 119 of them warranted). 101 are on intact Ch-1 objects, so the Archive's 1979 reply ("over a hundred intact objects") checks out.
- **Damage (Hallam predicted over-representation).** Objects bearing `-ar` are *more* often intact than other objects: 128/148 (86%) vs 179/230 (78%).
- **Broken halves (Hallam predicted "far above chance").** Only 4 of 149 `-ar` segments contain a broken half, against 97 of 268 other segments. P(≤4) ≈ 2×10⁻¹⁷, so it is far *below* chance.
- **Margins (the only place "margin" can be tested is inside chains).**
  - Of 31 in-chain tokens, **16 are medial**, meaning the record continues through the `-ar` node. Examples: CSC-1065 `larluki-in-ru · ru-yunpuru-ar-ru · ru-pusarsi-in`; CSC-1108 `tu-lanlartu-ar-ru · ru-telnuro-in`.
  - 6 more are chain-initial with an edge leaving, and only 9 are chain-final.
  - Medial share: 52% for `-ar` against 12% for all chain words (P ≈ 8×10⁻⁸).
- **Hand copies (the page-end argument).** Only 2 `-ar` tokens occur in the 15 Ch-2 hand copies, and one of them is medial (CSC-1108). The argument cannot be reproduced from the catalogue.
- **A positive structural signal.** 3 of the 7 BAR edges leave an `-ar` node (CSC-1121, -1165 the Ladder, -1176: `X-ar-pel · pe-Y`). Among all 182 chain-initial tails, only 6 are `-ar`. "A junction with a barred exit" is a coherent graph statement; "the record stops here" is not.
- **Limits.**
  - For the 123 one-word labels, the catalogue cannot tell "junction" from "rest not given here".
  - `figures.json` puts the junction map at 157 nodes, 153 of them (97%) junctions by `-ar` alone. The handbook says roughly 60% of 214. So the map's junctions rest on the marker with essentially no stated second edge anywhere.

### A3. Redfern 1993: is ADJ an edge class or a damage convention?

**Verdict: side 2 in substance. ADJ marks an edge that could not be read on a damaged object; it is not a class of the source. Confidence 0.9.**

Correction to Redfern: this is not only a nineteenth-century habit. 7 of the 15 ADJ objects came through the 1908 register consolidation (2 undated, 5 accessioned 1886–1903). The other 8 were accessioned and catalogued in 1939–2023, so the Standard's own transcribers still write it.

- **Inventory.** 18 halves on 15 objects, all Ch-1. No `yu-` head exists anywhere (`figures.json` adj_pairs = 0).
- **Every ADJ object is damaged:** fractured 4, eroded 5, worn 6, intact 0. The base rate is 205 intact out of 276 Ch-1 functional objects (74%), giving hypergeometric P ≈ 4×10⁻¹⁰. A source-system edge class cannot know whether its object will later fracture.
- **It never carries edge fields.** ADJ tails carry no grade or polarity (0/18), while 112/260 (43%) of other non-frozen tails do (P ≈ 4×10⁻⁵). That is what a placeholder for an unreadable edge looks like.
- **It produces every grammatical violation in the corpus.** All 11 "ill-formed" findings in the whole catalogue (E-CARRIER 8, E-OFF 3) sit in segments containing an ADJ half. The word after `-yun` either carries a coordinate with no head half (e.g. CSC-1054, -1124, -1341, -1409, -1552) or is an OFF node reached by a non-SIM edge (CSC-1049, -1362). Read ADJ as "an edge half stood here and is lost" and every one of these disappears: the head was lost with the edge.
- **Other damage signatures.** 13 of the 18 ADJ segments also lack a warrant (D-WARRANT).
- **Absent from the instrument channel.** The Ch-3 value slot has all six other classes across 81 edge-class tokens and never `yun`. At the I–II share of about 6%, 4–5 would be expected (P(0) ≈ 0.01).
- **Consequence.** The edge-class inventory is six. Any graph edge resting only on `-yun` is a hole. The handbook says 87 such edges; the catalogue has 18 halves.

### A4. The Ladder plaque: is `-sen` segment-scoped or edge-scoped?

**Verdict: leans side 2 (edge-scoped, Cardwell). The plaque itself (CSC-1165) cannot be settled. Confidence 0.6.**

- **Polarity is an edge field.** All 62 polarity tokens sit in a tail's suffix chain (INC-TAIL-(GRADE)-POL). None is free-standing.
- **Stratum II polarity behaves edge-scoped even without `-he`.** Stratum II puts *different* polarity values on different edges of the same segment:
  - CSC-1337: UNA on edge 1, FRB on edge 2, UNA on edge 4;
  - CSC-1328: UNA-EVERY on edge 1, FRB-EVERY on edge 2;
  - CSC-1310: UNA on edge 2 of 4 only.

  Read as segment-scoped, these segments contradict themselves.
- **`-he` does look like a pair-scope marker in Stratum I.** It has 7 tokens, always after a polarity. Five sit on complete edge pairs and two on tails whose head was lost to damage. It never appears on the 12 tail-only IMP tokens on Stratum I objects, which have no pair to scope over.
- **But segment scope is possible in principle.** Stratum I objects carry two complete-edge polarities without `-he`: CSC-1200 `lunkinu-in-tul-sen` and CSC-1149 `helusyu-in-tul-nir`. There is no Stratum I BAR+FRB record at all, so there is no parallel for the plaque.
- **The sealing formula does not decide it.** CSC-1012, "said when a locus is placed under containment", has the plaque's shape (BAR+FRB, `hilun-nu-hilun`). Containment fits "may go in, may not come back" as well as "withheld".
- **The Hallam variant (the dispute has no object) is disfavoured** by A2.
- **Aside.** The only root pair recorded with two different edge classes is the Ladder's own: `harnuli→kurhali` is BAR in CSC-1165 and SHUNT in CSC-1530 (2014). Under a Locative reading that would be a traversal along the barred orientation. Under A8 the two records are unrelated.

### A5. Keele 1963: is `kalsira-ru` a frozen pair or a literal onward PASS edge?

**Verdict: side 1, frozen. Confidence 0.85.**

- **Inventory.** 29 `kalsira` tokens:
  - 24 are Stratum II `kalsira-ru` (18 Ch-1, 6 Ch-2).
  - 3 are ordinary compositional Stratum I uses: CSC-1407, -1448 and -1460 are all `kalsira-in-ru · ru-X=coordinate · tir lekur` and all completed.
- **Formal fingerprint.**
  - All 24 frozen tokens **lack an incidence marker**. No other Ch-1 or Ch-2 word has that shape; the only other cases are two Ch-4 formula words.
  - 8 frozen tokens carry an incoming head (`ru-/ke-/tu-kalsira-ru`), yet lack the MED marker that every genuine medial node carries.
- **Placement.** All 24 are on intact objects, always segment-final with a warrant present. No other damage finding appears on any of those objects (0/24).
- **The break inventory partitions perfectly by condition.** Of the 101 broken-half findings:
  - the 66 on intact objects are exactly three fixed constructions: `kalsira-ru` 24, `lartuki-halu` 19, and IMP tails (`-ru-mun`/`-ken-mun`) 23;
  - all 35 others are on damaged objects.

  `kalsira-ru` classes with the explicit "no such departure" construction, not with damage.
- **It patterns with terminus records.** 11 of the 18 Ch-1 objects ending in `kalsira-ru` carry a Stratum III field (61%), against 11 of 55 ending in ordinary complete chains (20%). Fisher p ≈ 0.002.
- **What cannot be shown.** The corpus cannot prove the meaning is "sanction ends here" rather than "a sanctioned edge leaves to an unrecorded destination". But the latter would make it the only incidence-less, polarity-less dangling PASS tail on an intact record in the corpus.
- **Note.** L-16 (Quiet Sixteen) holds three `kalsira-ru` records (CSC-1068, -1287, -1459), the most at any locus.

### A6. Sturge 1958: is a multi-edge coordinate measured from the preceding tail-bearer or the chain-initial node?

**Verdict: undecidable from this corpus. Confidence 0.75 that it is undecidable.**

- `figures.json` lists 12 multi-edge coordinate segments. 10 have an unbroken chain from word 1: CSC-1104, -1172, -1191, -1193, -1289, -1299, -1310, -1345, -1415, -1470.
- **An indirect test.** In single-edge segments, PHASE depends on edge class: BIND always gives `kihar` (6/6), BAR always `hilun` (5/5), and SHUNT gives `nikur` 2 of 7 times and never `kihar`.
- I scored the 10 chains two ways:
  - Using the class of the last edge (the Standard) versus the first edge (Sturge), the likelihood ratio is about 8 for the Standard. It is driven mainly by CSC-1470 (PASS then SHUNT, giving `nikur`) and CSC-1299 (SHUNT then SIM-PASS, giving `kihar`, which SHUNT legs never take).
  - Using the anchor's grade instead, the ratio is about 0.4, the other way.
- Two proxies disagree on 10 cases, and the corpus has no magnitude to settle it. If forced, the lean is to the Standard.

### A7. The 1969 `lartuki-halu` paraphrase: right or wrong?

**Verdict: split.** The structural claims are right (confidence 0.8). The semantic content, "the attendance-state lapsed and was not resumed", is unsupported (undecidable, 0.5), and one sub-claim is misleading.

**What holds up:**
- All 19 have the form `HEAD-lartuki-in-halu=hilun-nu-hilun · W`.
- They are Stratum II only, all 19 on intact objects, all 19 with coordinate `hilun-nu-hilun`.
- No `ha-` head exists anywhere.
- Warrants are only `tir` (12) or `nes` (7); never `hos`, `lekur` or `wal`.
- They are the **only words in the corpus that carry both a head and a tail and are marked TERM**. Every other head+tail word is MED or JCT (or, for `kalsira`, unmarked). TERM plus a dangling tail means the chain ends here, so the `-halu` projects no edge. The Archive is right that "on the frozen reading none is broken".
- **Distributionally a terminus.** It is one of the three intact-object dangling constructions (A5). It carries a Stratum III field on 6 of 14 Ch-1 objects (43%), against 20% for ordinary chains (p ≈ 0.08). That fits a "not continued" sense, which is the paraphrase's direction.

**What does not:**
- Nothing in the formatives says *lapsed*. The notation has a dedicated LAPSED value, `-sar` (8 tokens). It occurs only after a committed grade (EXEC or AUTH) and never with `lartuki`.
- "No edge is claimed" is true only of the `-halu`. Every token records an incoming PASS, THRU or SHUNT edge *into* `lartuki` on "another pass". A "lapse" reading has to account for a recorded arrival into the attendance state, and the paraphrase does not.
- The root gloss "attendance" comes from the custodial formula's occasion (see B), so the paraphrase rests on a circular gloss.

### A8. Locative vs Stative: do roots name places or states?

**Verdict: side 2. Roots do not behave like node or place designators. Whether they are "states", rather than some other type label, is not demonstrable. Confidence 0.7.**

- **Roots do not track find-loci.**
  - Across 216 loci, same-root-same-locus repeats number 9 against 6.9 expected under shuffling (p ≈ 0.25). For one-word labels the figures are 2 against 0.85 (p ≈ 0.21).
  - Of the 55 loci holding two or more labels, 53 show only different roots. For example, L-99 has pularsi, isyuhi, tulanhe, tulkahe and toyunli.
  - Conversely, `kihetirlu` labels sit at 5 loci, `kastuhe` at 5 and `arhesi` at 4.
- **The graph never re-observes itself.**
  - 189 complete root-to-root edges contain 188 distinct ones. The single repeat is `kenutulti→kalsira` (CSC-1432 at L-12, CSC-1459 at L-16).
  - A century of routing over a fixed, named graph should re-record common edges, especially when "held on multiple passes" (`lekur`) is attested 63 times.
- **Same root, two nodes.** CSC-1147 `arpepu-in-ru · arpepu-is-ru · ru-hekasni-in` runs a chain through two nodes with the same root. That is natural for states and a self-loop for names.
- **A contradiction under Locative.** The Ladder pair's two classes (A4) would conflict.
- **For Locative:** roots can fill the LOCUS slot of a coordinate, in 8 cases (e.g. CSC-1065 `=petelti-hilun-pukal`, CSC-1536 `=kihetirlu-to-hilun`). That is the only point in its favour.

### A9. The 1949 restyling of REG (`nes`)

**Verdict: leans side 1. "Registered by the system itself" fits the distribution better than "entered without a human attestor". Confidence 0.6, partly dependent on A0.**

- **It behaves like a primary provenance class.** `nes` is the commonest warrant (115 tokens), yet it **never stacks** with another warrant: 0 of the 34 stacks (`lekur hos` 19, `hos lekur` 11, `tir lekur` 4).
  - A purely negative gloss ("no human attestor") should combine freely with "inferred" (`hos`), which is equally unattested. Instead `nes` and `hos` are mutually exclusive, as two different provenance sources would be.
- **Ch-3 uses only `nes` and `tir`.** The instrument logs use `nes` (7) and `tir` (4) as values and never `hos`, `lekur` or `wal`. At I–II warrant rates, P ≈ 0.001.
  - A machine stream using exactly {`nes`, `tir`} reads naturally as self-registered vs sensed-at-locus.
  - A gloss defined by the absence of a human attestor does no work in a stream where no record could have one.
- **Neutral evidence.** SIM (modelled) segments are warranted `nes` 6, `hos` 7, `tir` 0. That fits both glosses.
- The 1949 wording is the more cautious one, and was adopted for that reason. It is not the better fit to the data.

---

## B. Roots

**No clean top ten.** Token counts in Strata I–II (including the formulae) are: kalsira 29, lartuki 20, arhesi 12, kastuhe 8, silipelka 8, kihetirlu 8, then **seven roots tied at 7** (harnuli, yunpuru, arhisa, kurhali, senlihe, sahalustu, arlutu). I cover all 13.

**General findings:**

1. **Root meanings are not recoverable from this corpus, only their distributional roles.** Roots are also not tied to find-loci (A8).
2. **Many glosses are back-formed from the rituals, which is circular.**
   - 14 of the 35 roots graded G3 in the register appear in the Ch-4 formulae, and 5 appear *only* there: lankiro "kept", kanirlu "resting", yuntiha "waking", nirtoka "shut", lunpeki "twinned".
   - The glosses track the formula occasions:
     - `telnuro` "counted" → `siltoni` "passed" in *the count*;
     - `inpelu` "lost" in *the roll* ("after the names of those who did not return");
     - `nirtoka` "shut" → `olsihe` "still" in *the sealing*;
     - `kanirlu` "resting" → `yuntiha` "waking" in *the waiting*;
     - `sarkile` "bearing" → `lartuki` "attendance" in *the custodial attestation*.
   - For roots attested only in Ch-4, the ritual occasion is the only possible source of the gloss. The formula is then "translated" with that gloss.
3. **The register contains unsupported entries.**
   - 11 "core" roots have no catalogue attestation at all. Four of them carry G3 glosses: kentuli "forked", rasilke "early", sihoslu "first", munhilu "outer".
   - CSC-0141 `hitulke` has a distributional note ("always TERM, never carries a coordinate") with zero tokens behind it.
   - The channel field is wrong for 20 roots. For example, lankiro, kanirlu, nirtoka, lunpeki and yuntiha are listed as Ch-1/Ch-2 but occur only in Ch-4.
   - CSC-0016 `hasilnu`'s note ("the commonest root at loci the map shows with no outbound edge") rests on one locus-bearing token (CSC-1331).

| Root (n) | What the corpus shows | Archive gloss | Assessment |
|---|---|---|---|
| **kalsira** CSC-0012 (29) | 24 frozen `kalsira-ru` (A5). 3 ordinary Stratum I PASS origins, all `tir lekur`. 1 SHUNT-EXEC-LAPSED origin (CSC-1065). 1 destination (CSC-1191). All 29 intact, spread over 26 loci. Correlates with the end of sanctioned routes and with Stratum III fields | "sealed" | **Partly right.** It fits the frozen pair, but the root also starts ordinary onward edges in Stratum I. The gloss is the pair's meaning projected onto the root |
| **lartuki** CSC-0077 (20) | 19 frozen terminal construction (A7), plus BIND/OFF in the custodial formula. Always reached "on another pass", warranted only `tir`/`nes`, carries a Stratum III field in 6 of 14 | "attendance" | **Unverifiable and circular** (taken from the custodial formula's occasion) |
| **arhesi** CSC-0038 (12) | Vowel-initial. Never bears a head half (0/12): the head is missing in the one clean Stratum II arrival (CSC-1132), and in two others it follows ADJ damage. 5 `-ar` labels. FRB origin under `[41]` (CSC-1128). 12 loci | "common" | **Unsupported.** It looks like a label for the root's frequency |
| **kastuhe** CSC-0039 (8) | Mainly a label root (4 `-ar`, 1 `-in`). SIM origin to an OFF node (CSC-1197). Destination of a SHUNT edge (CSC-1341) and of a PASS leaving an EXEC-LAPSED node (CSC-1414). `wal` twice | none (G1) | **The Archive's stance is right** |
| **silipelka** CSC-0076 (8, plus 1 LOCUS use in CSC-1193) | 4 labels. Both of its destination coordinates are displaced (CSC-1369 `nu-rolun`, CSC-1470 `sa-nikur`). Origin into `lartuki-halu` (CSC-1454) | none | **Right to leave it unglossed** |
| **kihetirlu** CSC-0079 (8, plus 1 LOCUS use in CSC-1536) | Mostly junction labels (5/8 `-ar`). `tir`-warranted 5 of 8 (base rate about 25%). BIND origin to OFF (CSC-1471) | none | **Right** |
| **harnuli** CSC-0007 (7) | **Never a destination (0/7 heads).** Always an origin or label, with four edge classes leaving it (PASS in two formulae, BAR+FRB, THRU, SHUNT) and 3 `-ar`. Found at 5 loci | "in.standing" | **Gloss unverifiable; the origin-only role fits it.** The register's Locative note ("designates one node") is contradicted by its 5 loci and by its place at the head of the departure formula, which is said at every departure |
| **yunpuru** CSC-0011 (7) | Route-internal: medial JCT with edges in and out (3/7). SIM (modelled) edges on 3/7. EXEC-STANDING origin (CSC-1065). Correlates with modelled or planned chains | none | **Right** |
| **arhisa** CSC-0021 (7) | Vowel-initial. 3 `-ar` labels. Loses its head in Stratum II environments (CSC-1337, -1527). FRB origin (CSC-1337) | none | **Right** |
| **kurhali** CSC-0104 (7) | Two IMP tail-only origins ("no such departure": CSC-1223, -1388). Destination of BAR+FRB (the Ladder) and of SHUNT (CSC-1530). BIND origin. OFF under ADJ damage. Correlates with no-exit and closure records | "unattended" | **No support.** The implied opposition to `lartuki` "attendance" is invisible in the data: the two roots never co-occur |
| **senlihe** CSC-0041 (7) | UNA origins twice. Labels. OFF destination of a SHUNT-SIM edge (CSC-1314) | "turning" | **No support** |
| **sahalustu** CSC-0090 (7) | Destination of displaced edges (CSC-1097 SHUNT to `sa-nikur`) and of PASS edges. SHUNT origin into frozen `kalsira-ru` (CSC-1472). 3 of 7 on damaged objects | none | **Right** |
| **arlutu** CSC-0219 (7) | Vowel-initial. UNA-EVERY origins twice (CSC-1291, -1500: "unavailable, every time"). OFF (CSC-1295). Labels | "old" (G4) | **No support** |

---

## C. [41]

**What can be established:**

- **Occurrence and position.**
  - 12 tokens: all 9 formulae, plus 3 Ch-1 objects: CSC-1121 (L-311, accessioned 1886, Stratum I), CSC-1128 (L-350, 1889, Stratum II) and CSC-1325 (L-140, 1943, Stratum II). All three objects are intact.
  - Always segment-final in the warrant slot, and never combined with another warrant.
  - In Ch-4 a ritual unit always precedes it; in Ch-1 it follows the last node word directly.
- **In writing it occurs only on closure records.**
  - CSC-1121 has a BAR edge: `tiluyunhe-ar-pel · pe-pelra-in=hilun-nu-hilun`.
  - CSC-1128 has FRB: `arhesi-in-ru-sen · ru-telnuro-in`.
  - CSC-1325 has FRB plus ONCE: `larluki-in-halu-sen-li · ha-munkaru-in=hilun-nu-hilun`.
  - Only 13 of 354 warranted Ch-1/Ch-2 segments carry BAR or FRB, so three random ones would all do so with P ≈ 4×10⁻⁵.
  - Two of the three share the sealing formula's shape and coordinate (`hilun-nu-hilun`).
- **In recitation it is invariant and outside the metre.** It is present in 9/9 formulae, and the cola (7·7·4, 6·6·6, 7·7·6) sum to 18 or 20 without it. As a field it carries zero information in Ch-4. It behaves like a frame terminator or trailer that is excluded from the length count.
- **The ritual-unit slot before it co-varies with polarity.** `tuwalsi` occurs exactly on the two formulae with negative polarity (the sealing, BAR+FRB; the waiting, UNA+EVERY) and on no others.
- **It is not only a 19th-century copyist's artifact.** CSC-1325 was accessioned and catalogued in 1943, directly from an intact object and outside the 1908 register consolidation.
- **It sits in no series the published register contains.**
  - It is absent from Ch-2, Ch-3, Stratum III and the register.
  - The bracket convention ("cited by catalogue number") collides with the register, where **CSC-0041 is `senlihe` ("turning")**.

**What cannot be established:** any sound value or meaning.

**Supportable description:** a warrant-slot trailer that, in writing, marks closure or containment records and, in recitation, closes every formula.

---

## D. Stratum III

**The Archive's figures reproduce exactly:** 79 sequences, 707 tokens, 387 types, 381 found in only one sequence, P(recur within) 0.584, P(recur elsewhere) 0.040, 74/79 lengths divisible by 3, 85% of units coda-final, 3.06 syllables per unit on average.

**Structure found:**

1. **Templates.** Every sequence instantiates one of about 20 repetition templates, in three families:
   - **Group-final refrain** (41 sequences): ABCBDCAEC ×13, ABCDECAFC ×10, ABCBDCDECAFC ×5, ABCDEC ×5, ABCADC ×4, and longer variants.
   - **Mirror / palindrome** (15): ABCCBA ×7, ABCDADCBA ×5, ABCDEAAEDCBA ×2, and the 18-unit ABCDEFGABBAGFEDCBA (CSC-1294).
   - **Envelope / block repeat** (23): ABCADEABC ×6, ABCCDEECA ×5, ABCDAED ×3, ABCCAD ×3, and others.

   What recurs across records is the template; the units almost never do. The "exact thirds" claim is overstated: only 23 of the 39 nine-unit sequences have a single group-final refrain.
2. **The units themselves.**
   - Every unit is spellable from the 48-syllable list, and none is a functional root or formative.
   - Units within a sequence alliterate: a first syllable is shared by 8.2% of unit pairs within a sequence against 2.3% across sequences. Each sequence uses a restricted syllable palette (p ≈ 0.002).
   - There is no rhyme: last-syllable sharing is 2.8% within sequences against 3.7% across.
   - The penultimate unit is not systematically short (3.10 syllables vs 3.04), so CSC-1146's short `nusar` is not a rule.
3. **A few units recur across records.**
   - `tirakur` appears in four independent texts (CSC-1005, CSC-1146 = CSC-1258, CSC-1247/III, CSC-1283).
   - `nusar` appears in two (CSC-1146, CSC-1408/III), each time in the unique penultimate slot.
   - **`raken` (CSC-1182/III) and `sartel` (CSC-1472/III) are also Ch-3 vocabulary**, a key and a tail unit respectively. That is contact with Stratum IV, which the Stratum III volume says does not exist.
4. **Placement.**
   - Stratum III fields follow "terminus" records: `kalsira-ru` 11/18, IMP tails 8/23, `lartuki-halu` 6/14, SIM chains 5/14. Together that is 30/69 (43%), against 11/55 (20%) for ordinary complete chains (Fisher p ≈ 0.005).
   - A field never follows a label (0/128).
   - There is no locus-level association once the host objects are removed (p ≈ 0.23).
   - So the claim that Stratum III covaries with nothing is too strong: it covaries with what the record on the same object says.

**Decoding attempts, all negative:**

- **A cipher of the functional notation.** Excluded. The functional strata reuse 94% of their types across records, and any fixed-key encoding would carry that reuse over; Stratum III reuses 4%. A per-record key would be unbreakable here anyway.
- **An echo of the host record.** Host tail, grade, polarity and warrant syllables appear in their own Stratum III field 28 times out of 104 opportunities, against 28.6 expected (p ≈ 0.6). A crude syllable-overlap score shows a small excess (Jaccard 0.125 vs 0.099, p ≈ 0.014), but it does not survive decomposition (root syllables p ≈ 0.24, formative syllables p ≈ 0.07).
- **A magnitude table** (the missing PHASE quantity). Stratum III follows measured-displacement records only 3 times in 41 (CSC-1289, -1372, -1479).

**Verdict: no semantic reading is supportable.** What can be recovered is form (templates, alliteration, coda-heavy units), a handful of stock units, and placement after records that end something. The engineering reading is a fixed-frame payload appended to terminal status records. Whether that payload means anything cannot be decided from this corpus.

---

## E. The one thing the Archive has most wrong

**Keeping ADJ as an edge class, graded "contested G3", when its own catalogue settles the question.** This is the sharpest instance of a wider failure: **the Archive never checks its break and edge statistics against its own object-condition field.** Once that check is made, the catalogue separates damage from grammar with no exceptions:

- **ADJ.** It occurs only on damaged objects (15/15), never carries edge fields, is absent from the instrument channel, and produces every ill-formedness finding in the catalogue (11/11).
- **The break inventory.**
  - Of the 101 broken halves, the 66 on intact objects are exactly the three fixed constructions, and the 35 on damaged objects are genuine damage.
  - The real damage-break rate is therefore **35/417 = 8%**. The handbook says "~41% of sequences"; `figures.json` says 24%, which still counts the 66 fixed constructions.
  - The "remaining break inventory never re-audited" has now been audited. It hides no further frozen pairs.
- **Shadow segments.** §5.5 calls them "likeliest misparsed damage". In fact they are 12 formally complete records:
  - 9 are on intact objects, 11 have the head half on the OFF node, and none has a broken-half finding.
  - They follow a strict rule: every non-ADJ edge into an OFF node is BIND or SIM (23/23).

**Runners-up:**
- Onslow's "complementary distribution" is statistically empty, and his mechanism cannot produce post-1908 RECUR (A1).
- Root glosses are back-formed from ritual occasions (B).
- Stratum IV's membership is treated as open, while two of the Archive's own paradigm cells, PREP `-ka` and UNV `-lus`, are attested only in Ch-3 (A0).

---

## F. Method

**What I computed.**

- **Parsing** (`parse.py`). I split the Archive's gloss lines into head, root, suffix slots, coordinate, warrants and ritual units for all 417 segments. The suffix order is rigid (`slots.py`): INC-TAIL-[GRADE-[UNENT]-[DISCH]]-[POL-[RSCOPE]-[he]]. Constraints: discharge (`lun/sar/ro`) only after EXEC or AUTH, never after SIM (0/18); `kur/li` only after a polarity; `lar` only after AUTH. The §4.3 template omits these three slots, which `figures.json` calls "imports" (29 + 2 + 13 tokens).
- **Cross-tabulations** of every marker against condition, source, channel, stratum or profile, accession and catalogue year, and locus: `onslow.py`, `jct.py`, `adj.py`, `scope.py`, `warrants.py`, `headabs.py`, `breaks.py`, `dangling.py`, `efind.py`.
- **Exact and permutation tests:** hypergeometric and Fisher tests (`fisher.py`, `hallam.py`, `f41.py`), and shuffle tests for root–locus association (`locative.py`) and for Stratum III host echo (`iii2.py`, `iii3.py`, `iii5.py`).
- **Ch-3** (`ch3*.py`): triple segmentation, conditional entropies, (key, value) → tail consistency, and paradigm-by-key tables.
- **Coordinates** (`coords.py`, `sturge.py`): PHASE and PASS by closing edge class, and a smoothed likelihood comparison of the two anchoring rules.
- **Stratum III** (`iii*.py`): syllabification against the 48-syllable list (`syl.py`), template extraction, alliteration, palette and slot-length tests, and a check for shared vocabulary with every other stratum.
- **Graph consistency** (`edges.py`): edge recurrence and conflicting-class pairs.
- **Verified exactly** (`code.py`, `iii4.py`):
  - the handbook's error-detection claim for the 48-syllable list: 440 single-onset confusions, 334 (76%) detectable; open syllables 61%, closed 91%;
  - initial-syllable distinctness of the commanded core: 48 units with 48 distinct first syllables;
  - all the Stratum III figures in `figures.json`.

**Discrepancies between the handbook and the published figures or catalogue.** Many of the handbook's argumentative numbers are 2–9× larger than the catalogue supports:

| Item | Handbook | Published figures / catalogue |
|---|---|---|
| Broken-half rate | ~41% of sequences | 24.2%, of which 8% is real damage |
| SHUNT/RECUR edges | ~380 | 54 |
| Junction map | 214 nodes, ~60% by `-ar` only | 157 nodes, 97% by `-ar` only |
| ADJ-only edges | 87 | 18 halves |
| Stratum II head-absent environments | 212 / 148 / 63 / 85 / 31 | 24 / 13 / 4 / 9 / 2 |
| Longest sequence | 41, six over 30 | 25, none over 30 |
| Tokens in sequences of 3+ | ~2,900 | 4,012 |

Also:
- The handbook says the notch-count check cannot run on Ch-2, yet the register records "trace: short" verdicts for 9 Ch-2 plates.
- The Stratum II head-absence pattern itself is confirmed: head halves go missing only in Stratum II and only before vowel-initial roots (24 of 38 such edges), never in Stratum I (0/10). Whether that is loss or the 1908 cut, the catalogue cannot say.

**Limits.**
- I cannot see the traces, the junction map or outcome data.
- Every semantic question beyond distribution is outside what this packet can settle. Where I lean, the lean is stated with its confidence.
