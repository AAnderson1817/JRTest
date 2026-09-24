"""Phase 2: the build keeps its promises. Authority C.

Run with:  PYTHONPATH=. python3 -m unittest discover -s tests -p "test_*.py"
"""
import json
import shutil
import subprocess
import unittest
from pathlib import Path

import yaml

from hel import diachrony, field, parse, screen, verify
from hel.lexicon import default as lexicon

ROOT = Path(__file__).resolve().parent.parent


def catalogue():
    return json.loads((ROOT / "corpus" / "csc.json").read_text(encoding="utf-8"))


class Diachrony(unittest.TestCase):
    def test_laws_clean(self):
        self.assertEqual(diachrony.d1_check(), [])
        self.assertEqual(diachrony.d2_check(), [])

    def test_algonquian_constraint(self):
        forms = [r["second"] for r in diachrony.d2_table()] + [r["common"][1:] for r in diachrony.d2_table()]
        self.assertEqual(diachrony.algonquian_check(forms), [])

    def test_relative_chronology(self):
        ken = [r for r in diachrony.d2_table() if r["code_1988"] == "ken"][0]
        self.assertEqual(ken["second"], "kin")          # not hin: S2 is older than S3

    def test_second_branch_keeps_sen(self):            # F-27
        sen = [r for r in diachrony.d2_table() if r["code_1988"] == "sen"][0]
        self.assertEqual(sen["second"], "sen")

    def test_coda_counts(self):
        self.assertEqual(diachrony.coda_count_1908(), (3, 47, 47))


class FieldEnglish(unittest.TestCase):
    def test_register_validates(self):
        self.assertEqual(field.validate(), [])

    def test_inflection_is_ascii(self):
        self.assertEqual(field.inflect("kalsira", "past"), "kalsiraed")
        self.assertEqual(field.inflect("tul", "past"), "tulled")

    def test_naming_rules(self):
        import random
        for kind in ("shape", "find", "interval", "failure"):
            n = field.name(kind, random.Random(1))
            self.assertEqual(n["rule"], kind)
            self.assertTrue(n["name"])

    def test_wall_reads_back_the_roll(self):
        wall = yaml.safe_load((ROOT / "data" / "wall.yaml").read_text(encoding="utf-8"))
        op = [l["t"] for l in wall["lines"] if l["k"] == "op"][0]
        self.assertEqual(op, "Locus open, pass other, phase displaced.")


class Screen(unittest.TestCase):
    def test_structural(self):                         # F-26
        self.assertFalse(screen.passes("kashira"))
        self.assertFalse(screen.passes("haarlun"))
        self.assertTrue(screen.passes("harnuli"))

    def test_known_rejects(self):                      # A-reserve §10's own examples
        for f in ("pelusar", "penisar", "walniken", "pelunar"):
            self.assertFalse(screen.passes(f), f)

    def test_fixed_forms_disclosed(self):
        """Only the adjudicated fixed forms reach rejection weight (docs/08 §5)."""
        hits = set()
        for cls, forms in screen.canon_forms().items():
            rep = screen.report([f.lower() for f in forms], bound=cls == "bound formatives")
            hits |= set(rep["rejected"])
        self.assertEqual(hits, {"nikur", "vance"})

    def test_every_coined_form_passes(self):
        reg = json.loads((ROOT / "corpus" / "register.json").read_text(encoding="utf-8"))["units"]
        iii = {u for e in catalogue() if e["stratum"].startswith("III") for u in e["units"]}
        core = {u["form"] for u in reg if u.get("core") or u["kind"] == "ritual"}
        coined = {u["form"] for u in reg} - core
        self.assertEqual([f for f in sorted(coined | iii) if not screen.passes(f)], [])


class Corpus(unittest.TestCase):
    def test_nothing_sealed_in_the_catalogue(self):
        key = yaml.safe_load((ROOT / "sealed" / "key.yaml").read_text(encoding="utf-8"))
        text = (ROOT / "corpus" / "csc.json").read_text(encoding="utf-8")
        for form, d in key["TRUTH"]["roots"].items():
            self.assertNotIn(d["def"], text, form)
        for k in ("TRUTH", "PRODUCTION", "WITHHOLDING", "sealed", "truth"):
            self.assertNotIn(f'"{k}"', text)

    def test_every_stratum_iii_entry_passes_the_classifier(self):   # F-21
        lex = lexicon()
        for e in catalogue():
            if e["stratum"].startswith("III"):
                for u in e["units"]:
                    self.assertIsNone(parse.assignable(u, lex), (e["ref"], u))

    def test_verifier_has_no_failures(self):
        rows = verify.claims()
        self.assertEqual([r["id"] for r in rows if r["status"] == "fails"], [])
        self.assertEqual(sum(r["status"] == "holds" for r in rows), 37)

    def test_deterministic(self):
        from hel.corpus import Build
        a, b = Build().run(), Build().run()
        self.assertEqual(json.dumps(a.figures, sort_keys=True, default=str),
                         json.dumps(b.figures, sort_keys=True, default=str))
        self.assertEqual([e.ref for e in a.entries], [e.ref for e in b.entries])



class TrialFixes(unittest.TestCase):
    """critique/B1: the production defects the blind trial found stay fixed."""

    def test_41_carries_no_polarity(self):              # F-30
        for e in catalogue():
            for s in e["segments"]:
                if "[41]" in s["translit"] and e["channel"] == "Ch-1":
                    seg = parse.parse_segment(s["translit"], lexicon())
                    self.assertFalse(any(w.polarity for w in seg.words), e["ref"])

    def test_ritual_units_do_not_track_polarity(self):  # F-30
        F = yaml.safe_load((ROOT / "data" / "formulae.yaml").read_text(encoding="utf-8"))["formulae"]
        by_unit = {}
        for f in F:
            seg = parse.parse_segment(f["text"], lexicon())
            by_unit.setdefault(seg.free[0], set()).add(any(w.polarity for w in seg.words))
        self.assertTrue(all(len(v) == 2 or len(v) == 1 and False in v for v in by_unit.values()), by_unit)

    def test_nine_bound_pairs_rendered(self):           # F-31
        key = yaml.safe_load((ROOT / "sealed" / "key.yaml").read_text(encoding="utf-8"))
        text = (ROOT / "corpus" / "csc.json").read_text(encoding="utf-8")
        for bp in key["TRUTH"]["bound_pairs_unpublished"]:
            self.assertGreaterEqual(text.count(bp["pair"] + " "), 1, bp["pair"])

    def test_identified_constructions_are_not_damage(self):   # F-32
        from hel import grammar as g
        seg = parse.parse_segment("kalsira-ru · hos", lexicon())
        codes = [f.code for f in g.check(seg)]
        self.assertIn("N-PAIR", codes)
        self.assertNotIn("D-BROKEN", codes)
        seg = parse.parse_segment("hasilnu-tul · hos", lexicon())   # unidentified: still a break
        self.assertIn("D-BROKEN", [f.code for f in g.check(seg)])

@unittest.skipUnless(shutil.which("node"), "node not installed")
class BrowserEngine(unittest.TestCase):
    def test_agrees_with_python(self):
        r = subprocess.run(["node", str(ROOT / "tests" / "js" / "engine_check.js")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)


if __name__ == "__main__":
    unittest.main()
