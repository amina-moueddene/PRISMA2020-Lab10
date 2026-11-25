"""Tests du Lab 10 : présence des livrables, cohérence des données et du manuscrit."""
import json
import re
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
MAN = ROOT / "manuscript"
TEX = (MAN / "systematic_review_prisma2020.tex").read_text(encoding="utf-8")


class TestLab10Submission(unittest.TestCase):
    def test_manuscript_files_exist(self):
        for rel in ["manuscript/systematic_review_prisma2020.tex", "manuscript/systematic_review_prisma2020.pdf",
                    "manuscript/systematic_review_prisma2020.md", "manuscript/refs_included.bib",
                    "supplementary/checklist_prisma2020_27items.md", "supplementary/verification_finale_lab10.md",
                    "supplementary/validation_coherence_lab10.json"]:
            p = ROOT / rel
            self.assertTrue(p.exists(), f"Manquant : {rel}")
            self.assertGreater(p.stat().st_size, 300, f"Trop court : {rel}")

    def test_supplementary_data_s1_to_s5(self):
        expected = {"S1_screening_ledger.csv": 143, "S2_fulltext_eligibility.csv": 53,
                    "S3_fulltext_extraction_22_studies.csv": 22, "S4_quality_assessment_Q1-Q10.csv": 22,
                    "S5_studies_master_v2.csv": 22}
        for fname, n in expected.items():
            df = pd.read_csv(ROOT / "supplementary" / fname, encoding="utf-8-sig")
            self.assertEqual(len(df), n, fname)

    def test_every_included_figure_exists(self):
        figs = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", TEX)
        self.assertEqual(len(figs), 6)
        for fig in figs:
            self.assertTrue((ROOT / fig).exists(), f"Figure manquante : {fig}")
            png = (ROOT / fig).with_suffix(".png")
            self.assertTrue(png.exists() and png.stat().st_size > 20000, f"PNG manquant : {png.name}")

    def test_every_citation_is_in_bibliography(self):
        bib = (MAN / "refs_included.bib").read_text(encoding="utf-8")
        keys = set(re.findall(r"@\w+\{([^,]+),", bib))
        cited = {k.strip() for grp in re.findall(r"\\cite[tp]?\{([^}]+)\}", TEX) for k in grp.split(",")}
        self.assertFalse(cited - keys, f"Clés absentes du .bib : {sorted(cited - keys)}")

    def test_validation_report_status(self):
        rep = json.loads((ROOT / "supplementary" / "validation_coherence_lab10.json").read_text(encoding="utf-8"))
        self.assertEqual(rep["status"], "VALIDATED")
        self.assertEqual(rep["total_studies"], 22)
        self.assertEqual(rep["prisma_flow"]["identified"], 215)
        self.assertEqual(rep["prisma_flow"]["screened"], 143)

    def test_checklist_has_all_27_items(self):
        chk = (ROOT / "supplementary" / "checklist_prisma2020_27items.md").read_text(encoding="utf-8")
        for i in range(1, 28):
            self.assertRegex(chk, rf"\| {i}[a-f]? \|")

    def test_title_identifies_systematic_review(self):
        title = TEX.split("\\title{", 1)[1].split("}\n", 1)[0]
        self.assertIn("a systematic review of platforms", title)
        self.assertNotIn("mapping", title)

    def test_rounding_corrections_applied(self):
        self.assertNotIn("V=0.64", TEX)
        self.assertNotIn("0.64 (0.54)", TEX)
        self.assertNotIn("(0.52)", TEX)
        self.assertIn("0.63 (0.54); 0.002", TEX)
        self.assertIn("0.63 (0.51); 0.008", TEX)


if __name__ == "__main__":
    unittest.main()
