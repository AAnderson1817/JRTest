# Field English — the register that can grieve

> **Authority C throughout.** A design proposal for approval, not canon. Nothing here
> resolves an Authority D question, and nothing here is evidence about the substrate,
> its source, or whether anything built it. The data behind this document is
> `data/field_english.yaml` and `data/wall.yaml`; `hel/field.py` validates both on
> every build.

## 1. What it is

The substrate has no speakers. HEL does. Field English is the English its crews speak —
in debriefs, in the canteen, on a bad line at a departure locus — with substrate units
carried in it as loanwords. Crews call it *field*. The style manual calls it *Field
English (operational register)*.

It is the one place in the design with a speech community, and a speech community is
what a language needs in order to do the things this one has to do and the substrate
cannot: drift, joke, keep shibboleths, invent euphemisms and wear them out, name
things, and grieve. Phase 1 plan item 1 asked for exactly this, and for one test in
particular: **the register must be able to carry a lament.** Section 8 is the test.

What it must never do is carry evidence. A loan records what crews made of a unit.
It says nothing about what the unit is. The substrate's glosses stay where A §6.3 put
them, queried and graded; Field English sits beside them, confident and wrong in the
way working speech is.

## 2. How a unit becomes a word

Every loan took the same road, and the road is audible.

1. **The readback.** Route commands are confirmed by the double return (A §6.2): a
   coordinate comes back as *locus open, pass later, phase measured ahead*. Crews hear
   the readback words and the units under them hundreds of times.
2. **The debrief.** Units cross into English first in debrief transcripts, where a
   crew member reaching for a word for a missing colleague used the one the record
   used. The first attested case is 1919: a field notebook, a party whose fifth member
   did not return, and the word is *hilun*.
3. **The canteen.** English stress lands on the first syllable and the rest reduces.
   The 1949 Standard says *hiˈlun*, final stress, no reduction, ever; the canteen says
   *ˈhɪlən*. The distance between those two pronunciations is the register difference,
   and it is the first thing a newcomer learns to hear.
4. **The style manual.** It objects, and it loses. Section 4 of the 1949 manual:
   *"hilun is a statement about a record. A person is not a record."* Never enforced.

Loans are spelled without apostrophes, inflected or not — *kalsiraed*, never
*kalsira'd*; *tulled*, *tir*, *a hos route* — because the ASCII rule that governs every
substrate spelling governs the words crews made from them. The validator checks it.

**The one loan that never reduces** is *nikur* (PHASE.DISP.UNMEAS). Crews say it the
Standard way, *nɪˈkʊɹ*, even in the canteen, and newcomers who reduce it are corrected
once, quietly. The design reason is in `docs/08-THE-ENGINE.md` §5 (the collision
screen): the regular reduction would sit one voicing feature from an English slur. The
in-world reason is the one every speech community has for words like that. Nobody
writes it down.

## 3. The loans

Thirty-three in the register. The core of it:

| Loan | Field | From | The Archive's gloss | What crews mean | First |
| --- | --- | --- | --- | --- | --- |
| **hilun** | ˈhɪlən | `hilun` | GAP — the slot is unfilled, and the record says so | a member not returned and not known not to have come out; *go hilun*, *the hilun* | 1919 |
| **nu** | nu | `nu` | PASS.OTHER — another pass, order unrecovered | *on the nu*: some other pass; *see you on the nu* | 1934 |
| **lekur** | ˈlɛkəɹ | `lekur` | REP — held on multiple passes | a member who keeps coming back — admiring and uneasy at once | 1951 |
| **kalsira** | kælˈsiɹə | CSC-0012 | *sealed?* | the end of the line; where sanction stops; *kalsiraed* | 1963 |
| **tir** | tɪəɹ | `tir` | WIT — attested at the locus | seen on site | |
| **nes** | nɛs | `nes` | REG — entered without a human attestor | secondhand; on paper only | |
| **wal** | wɔl | `wal` | UNW — no source carried | rumour; *wal says* | |
| **hos** | hɔs | `hos` | INF — derived from other edges | worked out from the shape of things; *a hos route* | |
| **pukal** | ˈpukəl | `pukal` | PHASE.AHEAD.MEAS | came out later than you left; how much later, nobody can say | |
| **the second column** | | `pukal` | the magnitude column, printed empty since 1952 | a quantity everyone knows exists and nobody has | 1952 |
| **pel** | pɛl | `-pel` | BAR — present, not traversable this way | a one-way door | |
| **tul** | tʌl | `-tul` | SHUNT — arrival displaced from intent | to come out somewhere other than meant; *we got tulled* | |
| **halu** | ˈhælu | `-halu` | RECUR — a similar, non-identical return | the difference a returner brings back | |
| **sen / mun / nir** | sɛn · mʌn · nɪəɹ | polarity | FRB · IMP · UNA | closed · no such thing · not now (*nir season*) | |
| **ti / kas** | ti · kæs | grade | SIM · EXEC | a dry run · the go signal (*on kas*) | |
| **yun** | jʌn | `-yun` | ADJ? | a hole in the map | |
| **sil** | sɪl | `-sil` | BIND — one coordinate, two descriptions | two catalogue entries that turn out to be one place | |
| **ladder** (v.) | | CSC-0007 | the Ladder plaque | to act as though two incompatible readings both hold, to be safe | 1951 |
| **forty-one** (v.) | ˈfɔɹti ˈwʌn | `[41]` | no value assigned | to say the formula through to the end | |
| **tirakur** | ˌtɪɹəˈkʊɹ | CSC-1146 | none; Stratum III | to say the threshold text before entering a locus the map shows with no way out | |
| **a quiet sixteen** | | the 1961 incident | | a trip that went wrong because the map said something the record never did | |
| **G2** | | the grade | operationally validated | acted on for a century and never proven; works, nobody knows why | |
| **I came back with it** | | Sowerby, 1931 | | said of something brought back and not explained | |

Every entry in the data file also carries its history and, where there is one, what
the style manual says about it. Two histories worth reading whole:

**lekur.** The house rule that a segment warranted `lekur` alone is never translated
with *because* (A §4.5) became a proverb about luck: *Lekur isn't because.* It is said
to anyone with a long run of returns, usually by someone with a longer one.

**ladder.** The canteen minute book of 1951 records *laddering* — acting as if both
readings of the Ladder plaque hold at once, which is Field Protocol's own resolution of
the dispute (A §8 Example 2). The Archive calls it incoherent. Crews call it staying
alive.

## 4. The treadmill

Field Protocol forbids speaking `lan` (AUTH) within the stated distance of an active
locus (A §4.3). A word that cannot be said acquires substitutes, and each substitute
becomes as marked as the word it replaced:

| Years | What crews say instead of *lan* | Why it wore out |
| --- | --- | --- |
| before 1926 | *the permission* | became as marked as the word it replaced |
| 1926–1957 | *the third* | *grade three* in the readback; Treloar's discharge paper of 1926 made the grade a topic |
| 1957–1979 | *green* | retired when Thaxter's unentitled marker (1957) made *green* mean *green without the right to be* |
| 1979– | *the long word* | also the name of the one formula that carries it, which crews have not heard |

The dates are the diachronic layer's dates: 1926 and 1957 are when HEL's own analysts
found the discharge and unentitled markers (the Phase 1 imports H1 and H2). The
register's history is driven by the Archive's.

## 5. Shibboleths

| Feature | Chicago | 1949 Standard | Second branch |
| --- | --- | --- | --- |
| *e* and *o* | eɪ, oʊ | e, o | e, o (and raised when unstressed) |
| four recited units | *pel, pe, rosilpe, inpelu* | as Chicago | *fil, fi, rosilfi, infilu* |
| recitation stress | final (the Standard) | final | initial |
| old words | senior crews still say some retired 1908 strings; the Archive does not print them, and crews do not write them down | | |

A §6.2: you can tell where someone trained within one sentence. The p/f pair is the
famous one — Pellingham's correspondence of 1953 — and it is the subject of
`docs/09-DIACHRONY.md`.

## 6. Proverbs

- *Lekur isn't because.*
- *The record is reversible. The network is not.*
- *Every map has a second column.*
- *The map is not the itinerary.*
- *Hilun is a word for a record.*
- *Say forty-one.*
- *Sen which way?* — the Ladder dispute, compressed into a question
- *An ar is where the page ends.* — Hallam's reading, surviving as a joke about hand copies

## 7. Names

Archival names are generated by rule, not listed, and the rule is what makes a name
unrenameable once routes are catalogued under it (benchmark C13).

| Rule | Example | Why it sticks |
| --- | --- | --- |
| from a deprecated reading of a trace's shape | *the Ladder* | the reading is dead; the routes are catalogued under the name |
| from a find circumstance | *the 1897 underside* | the style manual's preference for anything without a reading |
| from an interval at a locus | *the Long Wait* (L-31) | outlives the crew and the interval |
| from a failure | *Quiet Sixteen* | a cover term: deliberately mundane, so that the failure has a name that says nothing |
| catalogue form | *CSC-1146* | always available, and stable by policy |

`hel.field.name(kind, rng)` coins a name by any of the four rules and returns the rule
with it; the Reading Room page has a button that does the same. Two things are never
named: Stratum III texts, with an evocative English title (A-reserve §7.1 — never *The
Lament of the Nine*), and places, after the missing.

## 8. The Reading at the Wall

Memorial Board 2 is in the Reading Room corridor. Everyone except the Archive calls it
the hilun wall. The reading is done on the first working day after a member is posted
hilun, by whoever last signed the route. The Archive has never authorised it and has
never asked anyone to stop.

> *The reader first reads the card pinned beside the board, where the style manual's
> authors put it.*
>
> **Hilun is a statement about a record. A person is not a record.**
>
> We read the hilun.
> Not the dead. We do not know that they are dead,
> and in this room not knowing is a thing you say out loud.
>
> `Locus open, pass other, phase displaced.`
>
> *The names. After each one, the room answers: hilun.*
>
> The slot is for where they came out.
> It is not empty. It is ruled empty.
> A worn slot is a loss. A ruled slot is a statement,
> and it is the only statement we have, so we make it.
>
> The table has a column for how far.
> It has been empty since nineteen fifty-two.
>
> Lekur isn't because. I know it.
> Most of us came back, and some of us came back more than once,
> and that was never a reason.
>
> So we carry them hilun. We do not carry them lost.
> Lost is a word for a map.
> Hilun is a word for a record,
> and a record can be read again, on another pass.
>
> See you on the nu.
>
> *The roll, in the branch the reader learned it in.*
>
> `inpelu-in-tul · tu-hasilnu-in=hilun-nu-nikur · lunkani ·`
>
> *(All:)* **Forty-one.**

### Performance notes

- **The card.** The 1949 manual wrote the sentence to stop crews using *hilun* of
  people. The Wall reads it aloud to keep the usage, so the reading begins with the
  Archive's own objection, in the Archive's own words.
- **The operational line is the roll's own coordinate**, read back the way a coordinate
  is confirmed over a bad line: level, three beats, no feeling put into it. It is the
  only line said that way, and it is the line people remember.
- **"Nineteen fifty-two"** is said in full, never "fifty-two". It is the year the route
  table was first printed with its magnitude column empty (A §5.2b).
- **The register switch.** In the English lines *hilun* is said the field way,
  [ˈhɪlən]. In the roll it is said the Standard way, [hiˈlun]. The switch is where the
  reading stops being about the people and becomes the record.
- **The roll** is recited in whichever branch the reader learned it in: Chicago, with
  its diphthongs, or the Second branch, with its *f* and without its head halves —
  *ˈinfilu-in-tul · ˈhasilnu-in=hilun-nu-nikur · ˈlunkani*. Nobody corrects anybody at
  the Wall.
- **The reader stops before [41].** The room says it.

### Why it is safe to ship

Every line that sounds like a claim is a claim about a record, and the register can
make no other kind. *The slot is for where they came out* is A's grammar: the LOCUS
slot of a coordinate states an emergence locus, and `hilun` rules it empty (A §5.2,
Example 1). *The table has a column for how far* is A §5.2b. *A record can be read
again, on another pass* is orientation-invariant reading and the PASS value `nu`.
Nothing in it says what the network is, whether anything built it, whether anyone is
listening, or where the missing are. It does not say they are alive. It says that
nobody may say they are not, and it makes that into the thing a room full of people can
hold together.

The operational English in the middle of it is the demonstration Phase 1 asked for: a
register built for route commands turns out to be the right register for grief,
because both are ways of stating exactly what is known and not one word more.

## 9. Ledger

New in Phase 2, all Authority C: the register and its two names; the loans and their
first attestations (the 1919 field notebook, the 1934 *nu*, the 1951 canteen minute
book); the 1949 style manual §4 and its sentence; the euphemism cycle and its dates;
the shibboleth table; the proverbs; the naming rules and generator; Memorial Board 2
and the reading at it; *nikur*'s unreduced stress. The custodial field paraphrase
*under attendance* depends on Authority B (custodianship) and stands or falls with it.
