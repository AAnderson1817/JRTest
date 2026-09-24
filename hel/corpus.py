"""Build the Consolidated Substrate Corpus.

    python3 -m hel.corpus            # writes corpus/csc.json, corpus/figures.json,
                                     # and sealed/truth.json

Authority C. The pipeline, in the only order it may run (benchmark Design rule 3):

    sealed key → world → render → damage → transcribe (1908) → catalogue → figures

Deterministic for a seed. Every published figure is computed from the catalogue this
module writes; none is typed in.
"""
from __future__ import annotations

import json
import random
from collections import Counter
from pathlib import Path

import yaml

from . import archive, coin, grammar as g, lexicon, parse, poetics, taphonomy
from .render import Renderer, Record
from .stratum_iv import IVGenerator
from .world import World, EPOCHS

ROOT = Path(__file__).resolve().parent.parent

# PRODUCTION parameters (no truth value): corpus shape only.
TARGET_TOKENS = 4300
CH2_FUNCTIONAL_TOKENS = 690
IV_LOGS = 64
P_STRATUM_I = 0.36
QUOTA = {
    "kalsira_completed": 3, "kalsira_frozen": 24, "lartuki_halu": 19, "half_negation": 23,
    "shadow": 14, "unent": 5, "authorization": 22, "bind": 16, "labels": 118,
    "stack": 37, "reversed": 14,   # tuned: the catalogue lands on A §4.5's 34 and 11
}
III_LENGTHS = [6] * 21 + [9] * 38 + [12] * 11 + [15] * 2 + [18] + [21]     # 74, all ≡ 0 mod 3
III_EXCEPTIONS = ["contested-7"] * 3 + ["extent-judged"] * 2


def accession_year(rng) -> int | None:
    band = rng.choices(("register", "1874", "1908", "1961"), (0.13, 0.25, 0.37, 0.25))[0]
    if band == "register":
        return None            # entered in a branch register before 1874; year not recorded
    return {"1874": rng.randint(1874, 1907), "1908": rng.randint(1908, 1960),
            "1961": rng.randint(1961, 2025)}[band]


class Build:
    def __init__(self, seed: int = 1908):
        self.seed = seed
        self.rng = random.Random(seed)
        self.world = World(seed)
        self.key = self.world.key
        self.lex = lexicon.load()
        self.core_roots = {d["feature"]: form for form, d in self.key["TRUTH"]["roots"].items()}
        self.rejects: dict = {}
        self._noncore()
        self.R = Renderer(self.world, self.core_roots, self.noncore, seed + 2)
        self.entries: list[archive.Entry] = []

    # ------------------------------------------------------------ the register
    def _noncore(self):
        rng = random.Random(self.seed + 1)
        w = self.world
        pair_freq = Counter()
        for v in range(1, len(w.loci)):
            for e in range(0, EPOCHS, 3):
                fs = sorted(w.features(v, e))
                for i, a in enumerate(fs):
                    for b in fs[i + 1:]:
                        pair_freq[(a, b)] += 1
        pairs = [p for p, c in pair_freq.items() if c >= 2]
        exclude = {u.form for u in self.lex.units} | set(poetics.CSC_1146) | {"nulisar"}
        forms = coin.coin_roots(760, rng, exclude, screen=True, rejects=self.rejects)
        weights = [1.0 for p in pairs]
        self.noncore = {f: rng.choices(pairs, weights)[0] for f in forms}

    # ------------------------------------------------------------ records
    def _route(self, e, s, st, start=None, length=None):
        for _ in range(8):
            r = self.R.route(e, s, start=start, length=length, stack_quota=st)
            if r is None:
                return None
            if not any((w.root == "kalsira" and w.tail == "PASS") or (w.root == "lartuki" and w.tail == "RECUR")
                       for w in r.seg.words):
                return r
        return None

    def _example1(self) -> Record:
        seg = parse.parse_segment(
            "harnuli-in-ken · ke-telnuro-is-ru · ru-kalsira-in=hilun-to-pukal · tir lekur", self.lex)
        w = self.world
        chain = None
        for v in sorted(w.forced_through):
            fin = [l for l in w.inn[v] if l.kind == "forced"]
            fout = [l for l in w.out[v] if l.kind == "direct" and w.loci[l.actual].dwell and l.sign == 1]
            if fin and fout:
                chain = (fin[0], fout[0])
                break
        return Record(seg, "route", 12, "I", {
            "loci": [chain[0].src, chain[0].actual, chain[1].actual] if chain else None,
            "links": [chain[0].lid, chain[1].lid] if chain else None,
            "features": ["standing_junction", "through", "held"], "made_at": True,
            "note": "A §8 Example 1, pinned verbatim"})

    def _ladder(self) -> Record:
        seg = parse.parse_segment("harnuli-ar-pel-sen · pe-kurhali-in=hilun-nu-hilun · hos", self.lex)
        w = self.world
        H, K = w.pins["ladder_H"], w.pins["ladder_K"]
        link = [l for l in w.out[K] if l.actual == H][0]
        return Record(seg, "status", 11, "II", {
            "loci": [H, K], "links": [link.lid], "features": ["standing_junction", "quiet"],
            "bar": True, "scope": "edge", "verdict": "Cardwell", "note": "A §8 Example 2, pinned verbatim"})

    def functional(self):
        rng, R = self.rng, self.R
        st = {"stack": QUOTA["stack"], "reversed": QUOTA["reversed"]}
        ch1, ch2 = [], []

        def ep():
            return rng.randrange(EPOCHS)

        def strat():
            return "I" if rng.random() < P_STRATUM_I else "II"

        ch1.append((self._example1(), {"pin": "example1", "condition": "intact", "year": 1911}))
        ch1.append((self._ladder(), {"pin": "ladder", "condition": "intact", "field_name": "the Ladder",
                                     "year": 1904}))
        q = R.kalsira_ru(ep(), completed=False, stratum="II")
        q.truth["loci"] = [self.world.pins["quiet_sixteen"]]
        # the cover term is the 1961 incident's; the marker it left from is catalogued under it
        ch1.append((q, {"pin": "quiet_sixteen", "condition": "intact", "year": 1936, "field_name": "Quiet Sixteen"}))
        for _ in range(QUOTA["kalsira_completed"]):
            ch1.append((R.kalsira_ru(ep(), completed=True, stratum="I"), {"condition": "intact", "single": True}))
        for i in range(QUOTA["kalsira_frozen"] - 1):
            (ch2 if i < 6 else ch1).append((R.kalsira_ru(ep(), completed=False, stratum="II"),
                                            {"condition": "intact", "single": True}))
        n = 0
        while n < QUOTA["lartuki_halu"]:
            r = R.lartuki_halu(ep(), "II")
            if r is None:
                continue
            (ch2 if n < 5 else ch1).append((r, {"condition": "intact", "single": True}))
            n += 1
        for _ in range(QUOTA["half_negation"]):
            ch1.append((R.half_negation(ep(), strat()), {"condition": "intact", "single": True}))
        for kind, k in (("shadow", QUOTA["shadow"]), ("unent", QUOTA["unent"]),
                        ("authorization", QUOTA["authorization"]), ("bind", QUOTA["bind"])):
            made = 0
            while made < k:
                if kind == "shadow":
                    r = R.shadow(ep(), strat())
                elif kind == "unent":
                    r = R.authorization(ep(), strat(), unent=True)
                elif kind == "authorization":
                    r = R.authorization(ep(), strat())
                else:
                    r = R.bind(ep(), strat())
                if r is not None:
                    ch1.append((r, {"single": kind in ("unent", "shadow")}))
                    made += 1
        for _ in range(QUOTA["labels"]):
            ch1.append((R.label(ep(), strat(), stack_quota=st),
                        {"condition": rng.choices(("intact", "worn"), (0.9, 0.1))[0], "label": True}))
        # [41] on three Ch-1 objects (A §4.5; sealed P-41): ordinary records whose warrant
        # slot holds the unit nobody can pronounce
        for _ in range(3):
            r = R.status(ep(), strat())
            while r is None:
                r = R.status(ep(), strat())
            r.seg.warrants = ["[41]"]
            ch1.append((r, {"condition": "intact", "single": True, "p41": True}))
        budget = TARGET_TOKENS - 700 - 610 - 100 - CH2_FUNCTIONAL_TOKENS
        used = sum(len(r.seg.tokens()) for r, _ in ch1)
        while used < budget:
            s = strat()
            r = self._route(ep(), s, st) if rng.random() < 0.58 else R.status(ep(), s, stack_quota=st)
            if r is None:
                continue
            ch1.append((r, {}))
            used += len(r.seg.tokens())
        used2 = sum(len(r.seg.tokens()) for r, _ in ch2)
        standing = [v for v in range(1, len(self.world.loci)) if self.world.loci[v].standing]
        while used2 < CH2_FUNCTIONAL_TOKENS:
            s = strat()
            v = rng.choice(standing)
            r = self._route(ep(), s, st, start=v, length=rng.choice((2, 2, 3))) if rng.random() < 0.6 \
                else R.label(ep(), s, locus=v, stack_quota=st)
            if r is None:
                continue
            ch2.append((r, {}))
            used2 += len(r.seg.tokens())
        return ch1, ch2

    # ------------------------------------------------------------ objects & history
    def _find_locus(self, rec: Record) -> int:
        w, rng = self.world, self.rng
        loci = rec.truth.get("loci") or []
        if rec.truth.get("made_at", rng.random() < 0.6) and loci:
            return loci[0]
        cand = list(range(1, len(w.loci)))
        return rng.choices(cand, [w.loci[v].find_rich for v in cand])[0]

    def assemble(self):
        rng = self.rng
        ch1, ch2 = self.functional()
        objects = []            # dicts: channel, source, records, meta, locus, year
        # Ch-1 objects: pinned and labels alone; the rest grouped 1-3 records per object
        singles = [(r, m) for r, m in ch1 if m.get("pin") or m.get("label") or m.get("single")]
        pool = [(r, m) for r, m in ch1 if not (m.get("pin") or m.get("label") or m.get("single"))]
        rng.shuffle(pool)
        for r, m in singles:
            objects.append({"channel": "Ch-1", "source": "object", "records": [r], "meta": m})
        i = 0
        while i < len(pool):
            k = rng.choices((1, 2, 3), (0.74, 0.21, 0.05))[0]
            grp = pool[i:i + k]
            i += k
            strat_ = grp[0][0].stratum
            recs = []
            for r, m in grp:
                r.stratum = strat_
                recs.append(r)
            meta = dict(grp[0][1])
            objects.append({"channel": "Ch-1", "source": "object", "records": recs, "meta": meta})
        for r, m in ch2:
            objects.append({"channel": "Ch-2", "source": "plate", "records": [r], "meta": m})
        # history: find locus and accession year
        for k, o in enumerate(objects):
            o["obj"] = f"obj-{k:04d}"
            o["locus"] = self._find_locus(o["records"][0])
            m = o["meta"]
            if o["channel"] == "Ch-2":
                # counted records travel on photographic plates: a copyist's h/k swap would
                # change the unit the documents count (A §10.1b's nineteen)
                y = rng.randint(1890 if m.get("single") else 1861, 2025)
                o["year"] = y
                o["source"] = "hand copy" if y < 1890 else "plate"
                o["copy_generations"] = rng.choice((1, 2, 2, 3)) if y < 1890 else 0
            else:
                o["year"] = m.get("year", accession_year(rng))
            if m.get("pin") == "quiet_sixteen":
                o["locus"] = self.world.pins["quiet_sixteen"]
            if m.get("pin") == "ladder":
                o["locus"] = self.world.pins["ladder_H"]
        return objects

    def damage_and_transcribe(self, objects):
        rng = self.rng
        for o in objects:
            cond = o["meta"].get("condition") or (
                taphonomy.draw_condition(rng) if o["channel"] == "Ch-1" else "intact")
            o["condition"] = cond
            pre1908 = o["year"] is None or o["year"] < 1908
            segs, notes = [], {"env": [], "adj": 0, "copy": [], "page_end_ar": False}
            truths = []
            for j, r in enumerate(o["records"]):
                d = taphonomy.damage(r, cond, rng, last_on_object=(j == len(o["records"]) - 1))
                seg, nt = archive.transcribe(d, channel=o["channel"], source=o["source"], pre1908=pre1908,
                                             rng=rng, copy_generations=o.get("copy_generations", 0))
                segs.append(seg)
                notes["env"] += nt["env"]
                notes["adj"] += nt["adj"]
                notes["copy"] += nt["copy"]
                notes["page_end_ar"] |= nt["page_end_ar"]
                truths.append({"kind": r.kind, "epoch": r.epoch, "stratum_draw": r.stratum,
                               "damage": d.damage, **{k: v for k, v in r.truth.items()}})
            prof = [g.stratum_profile(s) for s in segs]
            stratum = o["records"][0].stratum
            o["entry"] = archive.Entry(
                cid="", channel=o["channel"], stratum=stratum, source=o["source"],
                locus=f"L-{o['locus']}", accession_year=o["year"],
                catalogued_year=(1908 if pre1908 else o["year"]), condition=cond, segments=segs,
                register=notes, field_name=o["meta"].get("field_name"), obj=o["obj"],
                sealed={"records": truths, "profiles": prof, "pin": o["meta"].get("pin")})
        return objects

    # ------------------------------------------------------------ Stratum III
    def stratum_iii(self, objects):
        rng = random.Random(self.seed + 3)
        exclude = {u.form for u in self.lex.units} | set(self.noncore)
        texts = []
        lens = list(III_LENGTHS)
        rng.shuffle(lens)
        shared = ["tirakur", "nusar"]            # CSC-1146 shares two types (A-reserve §8.2)
        forms = ("triad", "triad", "anaphora", "chain", "ring", "litany")
        for L in lens[:-2]:                      # 72 composed; with CSC-1146 and the second recitation, 74
            t = poetics.compose(rng.choice(forms), L // 3, rng, exclude | set(poetics.CSC_1146),
                                self.lex, shared_pool=shared, share_p=0.05)
            exclude |= set(t.units) - set(shared)
            texts.append(t)
        exc = []
        for kind in III_EXCEPTIONS:
            t = poetics.exception(kind, rng, exclude | set(poetics.CSC_1146), self.lex)
            exclude |= set(t.units)
            exc.append((kind, t))
        # placement
        ch1_objs = [o for o in objects if o["channel"] == "Ch-1" and not o["meta"].get("label")
                    and not o["meta"].get("pin") and o["condition"] == "intact"
                    and o["entry"].segments and o["entry"].segments[-1].warrants]
        rng.shuffle(ch1_objs)
        entries = []
        regular = list(texts)
        # 1. CSC-1146: no trace, L-31, 1897
        t1146 = poetics.csc_1146()
        entries.append(self._iii_entry(t1146, "Ch-1", "object", self.world.pins["long_wait"], 1897,
                                       "no trace", pin="csc_1146", catalogued=1952,
                                       field_name="the 1897 underside"))
        # 2. the two Ch-4 recitations: the threshold text (= the Sowerby text) and one other
        entries.append(self._iii_entry(t1146, "Ch-4", "recitation", None, 1931, "recitation", pin="threshold",
                                       catalogued=1952, field_name="the Sowerby recitation"))
        entries.append(self._iii_entry(regular.pop(), "Ch-4", "recitation", None, None, "recitation"))
        # 3. forty-one after a completed segment on a traced object
        for o in ch1_objs[:41]:
            t = regular.pop()
            host = o["entry"]
            host.locus = f"L-{self._iii_locus(rng)}"     # found where Stratum III is found
            e = self._iii_entry(t, "Ch-1", "object", None, host.accession_year, "after completed segment")
            e.locus, e.obj, e.part = host.locus, host.obj, "III"
            e.catalogued_year = max(host.catalogued_year, 1976) if host.catalogued_year < 1976 else host.catalogued_year
            entries.append(e)
            host.notes.append("carries a Stratum III field after its last completed segment")
        # 4. six Ch-2 plates (whole records): two are the extent-judged exceptions
        plates = [t for k, t in exc if k == "extent-judged"] + [regular.pop() for _ in range(4)]
        for t in plates:
            entries.append(self._iii_entry(t, "Ch-2", "plate", self._iii_locus(rng), rng.randint(1896, 2019),
                                           "whole record"))
        # 5. no-trace Ch-1 objects: the rest, including the three contested-7 provisionals
        for t in [t for k, t in exc if k == "contested-7"] + regular:
            entries.append(self._iii_entry(t, "Ch-1", "object", self._iii_locus(rng), accession_year(rng),
                                           "no trace"))
        return entries

    def _iii_locus(self, rng):
        """Stratum III comes from few loci, concentrated where expeditions dwell
        (A-reserve §4.4: the association may be entirely dwell time)."""
        if not hasattr(self, "_iii_pool"):
            w = self.world
            r = random.Random(self.seed + 6)
            closed = [v for v in range(1, len(w.loci)) if (not w.out[v] or w.loci[v].dwell) and v not in (31, 9)]
            other = [v for v in range(1, len(w.loci)) if v not in closed and v not in (31, 9)]
            self._iii_pool = [31, 9] + r.sample(closed, 17) + r.sample(other, 12)
            self._iii_w = [6, 3] + [2.2] * 17 + [1.0] * 12
            # A-reserve §4.4: "79 sequences from 31 loci" — every locus in the pool yields
            # at least one sequence; the rest follow dwell time
            self._iii_unused = [v for v in self._iii_pool if v != 31]
            r.shuffle(self._iii_unused)
        if self._iii_unused:
            return self._iii_unused.pop()
        return rng.choices(self._iii_pool, self._iii_w)[0]

    def _iii_entry(self, t, channel, source, locus, year, position, pin=None, catalogued=None, field_name=None):
        units = list(t.units)
        report = parse.FieldReport(intact=True, channel=channel,
                                   branch_traditions=2 if channel == "Ch-4" else 0)
        cls = parse.classify_iii(units, report, self.lex)
        # the classifier decides; the build never overrides it
        if not cls.klass.startswith("III"):
            raise RuntimeError(f"composed Stratum III text rejected by the classifier: {cls.reasons}")
        e = archive.Entry(
            cid="", channel=channel, stratum=cls.klass,
            source=source, locus=f"L-{locus}" if locus is not None else None, accession_year=year,
            catalogued_year=catalogued or (year if year and year >= 1908 else 1976),
            condition="intact", units=units, field_name=field_name, iii_position=position,
            sealed={"iii_rule": t.rule, "pin": pin, "classifier": cls.reasons})
        return e

    # ------------------------------------------------------------ Stratum IV
    def stratum_iv(self):
        rng = random.Random(self.seed + 4)
        w = self.world
        gen = IVGenerator(rng, self.lex, {u.form for u in self.lex.units} | set(self.noncore))
        mod = [l for l in w.links if w.loci[l.src].modulating]
        out = []
        for i in range(IV_LOGS):
            l = rng.choice(mod)
            frames = rng.choices((2, 3, 3, 4, 5), (10, 30, 30, 20, 10))[0]
            units = gen.log(l.kind, frames, contrast=(i < 2))
            y = rng.randint(1921, 2025)
            out.append(archive.Entry(cid="", channel="Ch-3", stratum="IV", source="log", locus=f"L-{l.src}",
                                     accession_year=y, catalogued_year=y, condition="intact", units=units,
                                     sealed={"link": l.lid, "production": "P-IV"}))
        self.iv_vocab = {"frames": gen.frames, "values": gen.values}
        return out

    # ------------------------------------------------------------ Ch-4 formulae
    def formulae(self):
        data = yaml.safe_load((ROOT / "data" / "formulae.yaml").read_text(encoding="utf-8"))["formulae"]
        out = []
        for f in data:
            seg = parse.parse_segment(f["text"], self.lex)
            prof = g.stratum_profile(seg)
            out.append(archive.Entry(cid="", channel="Ch-4", stratum="II" if prof == "II" else "I",
                                     source="recitation", locus=None, accession_year=None, catalogued_year=1908,
                                     condition="transmitted", segments=[seg], field_name=f["name"],
                                     notes=[f["use"]], sealed={"formula": f["id"], "production": "P-CH4"}))
        return out

    # ------------------------------------------------------------ numbering
    def number(self, entries):
        """The 1949 re-catalogue numbered every accession — corpus or not — in
        accession order, so non-corpus accessions leave gaps; an object accessioned in
        1897 and promoted in 1952 keeps the number its accession earned (CSC-1146).
        Sequences on one object share its number; a Stratum III field on a traced
        object is cited with the suffix /III."""
        rng = random.Random(self.seed + 5)
        for i, e in enumerate(entries):
            if not e.obj:
                e.obj = f"seq-{i:04d}"
        objs = {}
        for e in entries:
            objs.setdefault(e.obj, []).append(e)

        def key(item):
            es = item[1]
            y = min((x.accession_year for x in es if x.accession_year is not None), default=1800)
            return (y, 0 if es[0].channel == "Ch-4" else 1, rng.random())

        order = sorted(objs.items(), key=key)
        pin_i = next(i for i, (_, es) in enumerate(order) if any(x.sealed.get("pin") == "csc_1146" for x in es))
        if pin_i > 145:
            raise RuntimeError(f"{pin_i} corpus accessions precede the 1897 object; CSC-1146 cannot hold")
        gaps = 145 - pin_i
        num, placed = 1001, 0
        for i, (_, es) in enumerate(order):
            if i == pin_i:
                num += gaps - placed
                placed = gaps
            elif i < pin_i and placed < gaps and rng.random() < gaps / max(1, pin_i):
                num += 1
                placed += 1
            elif i > pin_i and rng.random() < 0.08:
                num += 1
            for x in es:
                x.cid = f"CSC-{num}"
            num += 1
        entries.sort(key=lambda x: (int(x.cid[4:]), x.part))
        pin = next(x for x in entries if x.sealed.get("pin") == "csc_1146")
        assert pin.cid == "CSC-1146", pin.cid
        return entries

    # ------------------------------------------------------------ run
    def run(self):
        objects = self.assemble()
        self.damage_and_transcribe(objects)
        iii = self.stratum_iii(objects)
        iv = self.stratum_iv()
        f4 = self.formulae()
        entries = [o["entry"] for o in objects] + iii + iv + f4
        self.number(entries)
        self.entries = entries
        self._register()
        forms = {u.form: u for u in self.lex.units}
        self.figures = archive.figures(entries, forms)
        self.iii_figures = archive.iii_figures(entries)
        return self


def _free_ids(used, n):
    out, k = [], 1
    while len(out) < n:
        cid = f"CSC-{k:04d}"
        if cid not in used:
            out.append(cid)
        k += 1
    return out


def _register_method(self):
    """The unit register: the designed core plus every non-core root the catalogue
    attests, numbered in order of first attestation (the 1908 consolidation order)."""
    attested = []
    seen = set()
    for e in self.entries:
        for s in e.segments:
            for w in s.words:
                for form in [w.root] + ([w.coord.locus] if w.coord and w.coord.locus not in (None, g.GAP) else []):
                    if form in self.noncore and form not in seen:
                        seen.add(form)
                        attested.append(form)
                    elif form not in self.noncore and form not in self.lex.by_form and form not in seen \
                            and form not in poetics.CSC_1146:
                        seen.add(form)
                        attested.append(form)          # a copyist's variant: exists only in a hand
    used = {u.cid for u in self.lex.units}
    ids = _free_ids(used, len(attested))
    units = list(self.lex.units)
    for cid, form in zip(ids, attested):
        copyist = form not in self.noncore
        units.append(lexicon.Unit(cid=cid, form=form, kind="root", gloss=None, grade="G1" if not copyist else "—",
                                  core=False, commanded=False, channels=(),
                                  note="exists only in a copyist's hand (A §2.3)" if copyist else ""))
    self.published_lexicon = lexicon.Lexicon(units)
    self.register_new = attested


Build._register = _register_method


def write(b, out_dir: Path = ROOT):
    from . import export
    pub = export.published(b)
    needles = {d["def"]: f"definition of {form}" for form, d in b.key["TRUTH"]["roots"].items()}
    needles.update({f"{a}&{c}": f"compound of {f}" for f, (a, c) in b.noncore.items()})
    needles.update({d["verdict"]: f"verdict on {d['id']}" for d in b.key["TRUTH"]["disputes"]})
    leaks = export.leak_check(pub, needles)
    if leaks:
        raise SystemExit("LEAK CHECK FAILED:\n  " + "\n  ".join(leaks[:20]))
    (out_dir / "corpus").mkdir(exist_ok=True)
    (out_dir / "corpus" / "csc.json").write_text(json.dumps(pub["catalogue"], ensure_ascii=False, indent=0))
    (out_dir / "corpus" / "figures.json").write_text(json.dumps(
        {"figures": pub["figures"], "iii": pub["iii_figures"]}, ensure_ascii=False, indent=1))
    lex_units = [{"cid": u.cid, "form": u.form, "kind": u.kind, "gloss": u.gloss, "grade": u.grade,
                  "core": u.core, "commanded": u.commanded, "channels": list(u.channels), "note": u.note,
                  "readings": u.readings} for u in b.published_lexicon.units]
    (out_dir / "corpus" / "register.json").write_text(json.dumps({"units": lex_units}, ensure_ascii=False, indent=0))
    truth = {
        "WARNING": "SEALED. Author-side. Never ship. See sealed/README.md.",
        "seed": b.seed,
        "noncore_roots": {f: list(p) for f, p in b.noncore.items() if f in set(b.register_new)},
        "entries": {e.ref: e.sealed for e in b.entries},
        "iv_vocab": b.iv_vocab,
        "coin_rejects": b.rejects,
    }
    (out_dir / "sealed" / "truth.json").write_text(json.dumps(truth, ensure_ascii=False, default=str))
    return pub


def main():
    import time
    t = time.time()
    b = Build().run()
    write(b)
    print(f"built {len(b.entries)} catalogue entries in {time.time() - t:.1f}s; "
          f"{len(b.published_lexicon.units)} registered units; leak check clean")
    print(json.dumps({k: b.figures[k] for k in ("tokens", "channel_share", "stratum_share")}))


if __name__ == "__main__":
    main()
