# SEALED — author-side. Not for shipping.

This directory is the Rosetta precondition of `docs/06-PHASE1-RECOMMENDATION.md` §6.1
(Q4 as amended): **the semantic truth of the analyzable core is fixed before any
corpus token exists, and the corpus is generated from it.** Nothing here is canon,
and nothing here may be quoted, paraphrased or hinted at in shipped material. The
export that feeds anything shipped (`hel/export.py`) strips every sealed field and
fails its own leak check if one survives.

`key.yaml` has three sections, and the difference between them is the most important
thing in the file.

| Section | What it is | Rosetta rule |
| --- | --- | --- |
| **TRUTH** | Facts the corpus is rendered from: what each core root correlates with in the network, what the paradigm really contains, which standing disputes are right. | Every future Rosetta object must agree with it. R1 and R2 may only ever confirm TRUTH items. |
| **PRODUCTION** | Procedures that make the data for questions the canon protects. They carry **no truth value**: the author holds no answer, by construction, and the generator was built so that none is implied. | No Rosetta object may touch a PRODUCTION item, ever — the same rule as `07-ROSETTA-OPTIONS.md` R-a for Stratum III, generalised. |
| **WITHHOLDING** | One entry per published gap: what exists, why it is withheld, and the in-world cause. Auditable by count (benchmark F2 countermeasure 1). | — |

**The line the whole file is drawn on.** TRUTH fixes *correlation*: records bearing a
root occur where the network is in a stated condition. It never fixes *reference* —
whether the corpus is about this network, and why the correlation holds, stays
Authority D (Phase 1 X4). It never fixes *authorship* — the builders are not
represented anywhere in this directory, not even as a placeholder.

Change a TRUTH value, rebuild the corpus (`python3 -m hel.corpus`), and run the verifier
(`python3 -m hel.verify`): it reports every published claim the change breaks. That is
what this file is for — the design stays revisable, and every revision has computed
consequences.
