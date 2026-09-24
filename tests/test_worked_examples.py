"""The engine must reproduce every worked example in the design documents verbatim.

If one of these fails, either the engine or the document is wrong, and the test
says which line to read.
"""
import unittest

from hel import grammar as g, parse, phonology as ph
from hel.lexicon import default as lexicon

LEX = lexicon()

EX1 = "harnuli-in-ken · ke-telnuro-is-ru · ru-kalsira-in=hilun-to-pukal · tir lekur"
EX2 = "harnuli-ar-pel-sen · pe-kurhali-in=hilun-nu-hilun · hos"
EX3 = "sarkile-in-sil · si-lartuki-ol=hilun-sa-kihar · lunkani · [41]"
CSC_1146 = "walnisen pehisar tirakur pekalar munlisen tirakur walnisen nusar tirakur".split()


class Example1(unittest.TestCase):
    """A §8 Example 1 — route label (Ch-1, Stratum I)."""

    def setUp(self):
        self.seg = parse.parse_segment(EX1, LEX)

    def test_round_trip(self):
        self.assertEqual(self.seg.translit(), EX1)

    def test_well_formed_and_edges(self):
        self.assertTrue(g.well_formed(self.seg))
        edges = [(e.origin, e.dest, e.cls, e.kind) for e in g.edges_of(self.seg)]
        self.assertEqual(edges, [(0, 1, "THRU", "complete"), (1, 2, "PASS", "complete")])

    def test_anchor_is_telnuro(self):
        # A §5.2a: carried by kalsira, measured from telnuro (the Standard's reading)
        into = [e for e in g.edges_of(self.seg) if e.dest == 2]
        self.assertEqual(self.seg.words[into[0].origin].root, "telnuro")

    def test_gloss_lines_match_A(self):
        cols = dict(g.gloss_lines(self.seg, LEX))
        self.assertEqual(cols["harnuli-in-ken"], "CSC.0007(in.standing?)-TERM-THRU.TAIL")
        self.assertEqual(cols["ke-telnuro-is-ru"], "THRU.HEAD-CSC.0031(counted?)-MED-PASS.TAIL")
        self.assertEqual(cols["ru-kalsira-in"], "PASS.HEAD-CSC.0012(sealed?)-TERM")
        self.assertEqual(cols["=hilun-to-pukal"], "=LOC.GAP-PASS.LATER-PHASE.AHEAD.MEAS?")
        self.assertEqual(cols["tir"], "WIT")
        self.assertEqual(cols["lekur"], "REP")

    def test_readback_matches_A_6_2(self):
        a, b, c = g.readback(self.seg)
        self.assertEqual(b, "Harnuli, terminal, edge seven. Telnuro, medial, edge one. "
                            "Kalsira, terminal. Locus open, pass later, phase measured ahead. "
                            "Witnessed, recurrent.")
        self.assertEqual(c, "Confirmed, edge seven, edge one.")

    def test_stratum_profile(self):
        self.assertEqual(g.stratum_profile(self.seg), "I")

    def test_fifteen_tokens(self):
        self.assertEqual(len(self.seg.tokens()), 15)

    def test_reversal_edit_does_not_compose(self):
        # A §3.5 / §5.2a: move the PASS tail onto kalsira; the coordinate collapses
        bad = g.reversal_edit(self.seg, edge_index=1)
        codes = {f.code for f in g.check(bad)}
        self.assertIn("E-ANCHOR", codes)
        self.assertFalse(g.well_formed(bad))


class Example2(unittest.TestCase):
    """A §8 Example 2 — the Ladder plaque (Ch-1, Stratum II)."""

    def setUp(self):
        self.seg = parse.parse_segment(EX2, LEX)

    def test_round_trip_and_form(self):
        self.assertEqual(self.seg.translit(), EX2)
        self.assertTrue(g.well_formed(self.seg))

    def test_gloss_lines_match_A(self):
        cols = dict(g.gloss_lines(self.seg, LEX))
        self.assertEqual(cols["harnuli-ar-pel-sen"], "CSC.0007(in.standing?)-JCT?-BAR.TAIL-FRB?")
        self.assertEqual(cols["pe-kurhali-in"], "BAR.HEAD-CSC.0104(unattended?)-TERM")
        self.assertEqual(cols["=hilun-nu-hilun"], "=LOC.GAP-PASS.OTHER-PHASE.GAP")
        self.assertEqual(cols["hos"], "INF")

    def test_scope_clitic_absent_so_stratum_II(self):
        self.assertFalse(any(w.scope for w in self.seg.words))
        self.assertEqual(g.stratum_profile(self.seg), "II")

    def test_three_of_six_analytic_elements_are_G3(self):
        # A: "-ar JCT, -sen FRB, and the root CSC.0007" are G3
        w = self.seg.words[0]
        self.assertEqual(g.INCIDENCE[w.incidence].grade, "G3")
        self.assertEqual(g.POLARITY[w.polarity].grade, "G3")
        self.assertEqual(LEX.by_form["harnuli"].grade, "G3")


class Example3(unittest.TestCase):
    """A §8 Example 3 — custodial attestation (Ch-4)."""

    def setUp(self):
        self.seg = parse.parse_segment(EX3, LEX)

    def test_round_trip_and_form(self):
        self.assertEqual(self.seg.translit(), EX3)
        self.assertTrue(g.well_formed(self.seg, channel="Ch-4"))

    def test_eighteen_syllables_7_7_4(self):
        sylls = [s for t in self.seg.tokens() if t != "[41]" for s in ph.syllables(t)]
        self.assertEqual(len(sylls), 18)
        # the cola: the first break inside si-lartuki, the second inside -kihar
        cola = ["".join(sylls[:7]), "".join(sylls[7:14]), "".join(sylls[14:])]
        self.assertTrue(cola[0].endswith("silar"))
        self.assertTrue(cola[1].endswith("ki") and cola[2].startswith("har"))

    def test_bind_on_off_is_legal(self):
        self.assertNotIn("E-OFF", {f.code for f in g.check(self.seg, "Ch-4")})

    def test_gloss(self):
        cols = dict(g.gloss_lines(self.seg, LEX))
        self.assertEqual(cols["sarkile-in-sil"], "CSC.0058(bearing?)-TERM-BIND.TAIL")
        self.assertEqual(cols["si-lartuki-ol"], "BIND.HEAD-CSC.0077(attendance?)-OFF")
        self.assertEqual(cols["=hilun-sa-kihar"], "=LOC.GAP-PASS.SAME-PHASE.SAME")
        self.assertEqual(cols["lunkani"], "CSC.0311(?)")
        self.assertEqual(cols["[41]"], "(warrant slot; no value assigned)")


class CSC1146(unittest.TestCase):
    """A-reserve §8 — the flagship Stratum III text."""

    def test_classifies_as_III(self):
        c = parse.classify_iii(CSC_1146, parse.FieldReport(intact=True), LEX)
        self.assertEqual(c.klass, "III", c.reasons)

    def test_no_unit_assignable(self):
        for u in set(CSC_1146):
            self.assertIsNone(parse.assignable(u, LEX), u)

    def test_pekalar_is_the_only_ambiguous_type(self):
        amb = [u for u in set(CSC_1146) if len(ph.segment(u)) > 1]
        self.assertEqual(amb, ["pekalar"])
        self.assertEqual(set(ph.segment("pekalar")), {("pe", "ka", "lar"), ("pe", "kal", "ar")})

    def test_1971_extraction_fails_on_address_not_spelling(self):
        # pe-kal-ar spells legally; 'pekal' is not a registered root, so -ar has no address
        self.assertFalse(LEX.is_registered_root("pekal"))

    def test_too_short_and_damaged_fail(self):
        self.assertEqual(parse.classify_iii(CSC_1146[:5], parse.FieldReport(), LEX).klass,
                         "unassigned, short")
        self.assertEqual(parse.classify_iii(CSC_1146, parse.FieldReport(intact=False), LEX).klass,
                         "not III")


class Phonology(unittest.TestCase):
    def test_confusion_table_matches_A_6_1b(self):
        t = ph.confusion_table()
        self.assertEqual((t["total"], t["detectable"]), (440, 334))
        self.assertEqual(tuple(t["open"]), (220, 134))
        self.assertEqual(tuple(t["closed"]), (220, 200))

    def test_commanded_core_is_full(self):
        free = [g.GAP] + list(g.PASS_VALUES) + list(g.PHASE_VALUES) + [w for w in g.WARRANTS if w != "[41]"]
        units = [u.form for u in LEX.commanded()] + free
        self.assertEqual(len(units), 48)
        self.assertEqual(ph.initial_distinctness(units), {})
        self.assertEqual(sorted(ph.first_syllable(u) for u in units), sorted(ph.SANCTIONED))

    def test_A_preamble_grade_counts(self):
        from collections import Counter
        self.assertEqual(Counter(gr for _, gr in g.A_PREAMBLE_ITEMS),
                         Counter({"G2": 15, "G1": 10, "G3": 9, "G5": 1}))


if __name__ == "__main__":
    unittest.main()
