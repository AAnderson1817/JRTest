# Design Brief — Alien Language Project, Horizon Expedition League

**Status:** FIXED CANON. Every contributor works against this file. Do not contradict it.
Anything not fixed here is open design space.

---

## 0. What we are building

A constructed alien language of Tolkien-grade depth for the **Horizon Expedition
League (HEL)** setting, with the rigor a linguist would demand and the usability a
player or reader would need.

The bar is explicit: **rival Tolkien.** That means matching what actually made his
languages great, and then beating them where a science-fiction language can.

### What made Tolkien's languages great (match these)
1. **Diachronic depth.** Not one language — a proto-language plus regular sound
   laws producing attested daughters. Etymology is the load-bearing structure.
2. **Root-based derivation.** A closed set of proto-roots generating thousands of
   words by transparent, repeatable processes.
3. **Phonaesthetic coherence.** A distinctive, deliberate, beautiful sound.
4. **A script**, designed as an artifact of its own culture.
5. **Literature in the language** — verse with real meter, worth reading aloud.
6. **Cultural embedding.** The language encodes a worldview, a history, a theology.
7. **Internal variation** — dialect, register, archaism, borrowing.

### Where we beat him (this is the differentiator)
Tolkien's languages are gloriously *human* — Finnish, Welsh, and Latin in fancy
dress. A first-contact language must be equally deep but **genuinely non-human in
its category structure**, while remaining learnable and speakable by humans.

- **Phonology derived from anatomy**, not from "human sounds that feel exotic."
- **Grammatical categories no human language has**, motivated by the speakers'
  biology and ecology — obligatory where we would find them optional, absent
  where we would find them indispensable.
- **Mechanical verifiability.** Every sound law is executable code; every lexicon
  entry is checked against it. Tolkien could not do this. We will.

---

## 1. Setting frame (FIXED)

- The **Horizon Expedition League (HEL)** is an interstellar survey consortium:
  scientific, chronically underfunded, politically fractious, and staffed by
  specialists who are better at fieldwork than at diplomacy. HEL contact protocol
  is *observe, document, do not intervene* — honored inconsistently.
- Contact occurs on a large, tidally locked moon of a gas giant. The giant hangs
  **permanently fixed in the sky** over one hemisphere and never moves.
- The speakers are an **amphibious species of the tidal margin** — the zone
  between the deep water and the dry.
- Tides driven by the gas giant are enormous and highly regular. The tidal cycle,
  not the solar day, is the fundamental unit of lived time.
- Eclipses — the giant occulting the sun — are frequent, dramatic, and
  mythologically central.

**Consequences that MUST be reflected in the language:**
- **Absolute deixis.** The gas giant never moves, so direction is reckoned
  against it, never against the speaker's body. There is no native "left/right."
- **Tidal time.** Tense/aspect and the calendar are anchored to the tidal cycle.
- **Sensory evidentiality.** The species has at least one sense humans lack
  (pressure/vibration reception through turbid water is the expected candidate).
  Information source is **obligatorily** marked on the verb, and the categories
  cut the world differently than any human evidential system.

---

## 2. Hard constraints (FIXED)

**C1 — Anatomical phonology.** The phoneme inventory must be *derived* from an
explicitly specified non-human vocal tract, documented organ by organ. It must
exclude at least one major human articulator class for a stated anatomical
reason, and include at least one contrast humans do not use phonemically.

**C2 — Human-speakable.** ≥90% of the inventory must be producible by an
untrained human adult after brief coaching. A romanization must exist that a
voice actor can sight-read. Aliens whose language cannot be spoken on screen are
useless to us.

**C3 — Diachronic architecture.** One reconstructed proto-language; an ordered,
regular set of sound laws; **two** attested daughter languages that differ as
much as Quenya differs from Sindarin; plus one **contact pidgin** with HEL
personnel. Exceptions to sound laws must be individually justified (borrowing,
analogy, taboo replacement) — never waved through.

**C4 — Mechanical verification.** The sound laws ship as a runnable derivation
engine. Every lexicon entry declares its proto-root, and the engine must
reproduce its attested form. A lexicon that fails the checker is a bug.

**C5 — Root discipline.** All native vocabulary derives from proto-roots by
documented processes. No word may be invented "because it sounds nice" without an
etymology. Loanwords are permitted but must be marked as such.

**C6 — Alien categories, learnable surface.** At least three grammatical
categories with no close human parallel, each motivated by biology, ecology, or
society — never arbitrary. But the learning curve must be navigable: a motivated
teenager should manage greetings and a short poem in an afternoon.

**C7 — Literature.** The corpus must include verse in a native meter that
survives being read aloud, with interlinear gloss and literary translation.

**C8 — Etymological endonym.** The language's own name, the species' name for
itself, and all proper nouns must be derivable from proto-roots. Nothing is named
by authorial fiat.

---

## 3. Deliverable layout

```
docs/      brief, charter, reference grammar, phonology, diachrony, learner primer
lexicon/   machine-readable root & word lists (source of truth for the checker)
corpus/    texts: verse, inscription, dialogue, HEL field transcripts
script/    writing system: glyph design, orthography, transliteration rules
tools/     derivation engine + validators
critique/  evaluation rounds and dispositions
```

## 4. Glossing and notation (FIXED)

- **Leipzig Glossing Rules**, strictly. Three lines minimum: romanization,
  morpheme gloss, free translation.
- IPA in `/slashes/` for phonemes, `[brackets]` for phones.
- Proto-forms prefixed `*`. Unattested-but-predicted forms prefixed `**`.
- Sound laws are numbered and cited by number (e.g. "by L7").
