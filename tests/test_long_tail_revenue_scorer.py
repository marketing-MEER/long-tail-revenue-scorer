import tempfile
import unittest
from pathlib import Path

import pandas as pd
from click.testing import CliRunner

from long_tail_revenue_scorer import cli, core

EXAMPLES = Path(__file__).parent.parent / "examples"


class ScoreTest(unittest.TestCase):
    def test_lengths_and_rates(self):
        self.assertEqual(core.bucket(2), "1-2 words")
        self.assertEqual(core.bucket(6), "3-6 words")
        self.assertEqual(core.bucket(9), "7+ words")
        df = core.score(pd.DataFrame({"keyword": ["crm", "best crm for dentists in small towns today"],
                                      "volume": [10000, 100]}), ctr=10, value=100)
        rates = dict(zip(df["keyword"], df["conversion_rate_pct"]))
        self.assertEqual(rates["crm"], 0.17)
        self.assertEqual(rates["best crm for dentists in small towns today"], 1.83)

    def test_revenue_math(self):
        df = core.score(pd.DataFrame({"keyword": ["crm pricing for startups"], "volume": [1000]}), ctr=10, value=50)
        row = df.iloc[0]
        # 1000 x 10% x 1.61% = 1.61 conversions, x 50 = 80.5
        self.assertAlmostEqual(row["est_conversions"], 1.61)
        self.assertAlmostEqual(row["est_revenue"], 80.5)
        self.assertEqual(row["revenue_score"], 100)
        self.assertEqual(row["tier"], "1 revenue priority")

    def test_intent_and_tiers(self):
        self.assertEqual(core.intent("best crm"), "buyer")
        self.assertEqual(core.intent("how to clean a pipeline"), "research")
        self.assertEqual(core.intent("topology basics"), "unclear")       # whole words only
        self.assertEqual(core.intent("how to estimate project costs"), "research")
        self.assertEqual(core.tier(2, "buyer"), "3 head term, buyer")
        self.assertEqual(core.tier(4, "research"), "2 long-tail support")
        self.assertEqual(core.tier(1, "unclear"), "4 head term, awareness")

    def test_empty(self):
        df = core.score(pd.DataFrame({"keyword": [], "volume": []}))
        self.assertTrue(df.empty)
        self.assertIn("revenue_score", df.columns)
        self.assertEqual(core.summary(df)["keywords"].sum(), 0)


class CliTest(unittest.TestCase):
    def test_example_writes_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "rev"
            res = CliRunner().invoke(cli.main, [str(EXAMPLES / "project_keywords.csv"), "-o", str(out)])
            self.assertEqual(res.exit_code, 0, res.output)
            self.assertIn("Long-tail revenue report", out.with_suffix(".html").read_text(encoding="utf-8"))
            self.assertTrue(out.with_suffix(".xlsx").exists())


if __name__ == "__main__":
    unittest.main()
