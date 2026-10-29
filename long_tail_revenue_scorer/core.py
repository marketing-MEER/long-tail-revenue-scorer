"""Score keywords by revenue potential from their length and buyer intent.

The conversion rate for each keyword length is NP Digital's measured rate (paid search, 40 companies,
branded terms excluded). Estimated conversions = volume x your expected CTR x that rate, and estimated
revenue = conversions x your value per conversion. CTR and value are your own inputs, so the money
figures are a planning estimate for ranking the list, not a forecast.
"""
import re

import pandas as pd

from .report import find_column, to_number

# Conversion rate (%) by number of words, NP Digital, May 2025.
# Source: https://neilpatel.com/marketing-stats/conversion-rate-by-keyword-length/
CONV_RATE = {1: 0.17, 2: 0.35, 3: 1.02, 4: 1.61, 5: 1.58, 6: 1.94, 7: 1.83}

# Share of revenue by length bucket, for the summary.
# Source: https://neilpatel.com/marketing-stats/keyword-length-revenue-impact/ (NP Digital, August 2025)
BUCKETS = ["1-2 words", "3-6 words", "7+ words"]
NP_REVENUE_SHARE = {"1-2 words": "under 6%", "3-6 words": "around 45%", "7+ words": "over 50% by 2025"}

# Words that show someone is choosing or buying (general best practice, same idea as the
# keyword-intent-classifier repo). Whole words only.
BUYER = ["buy", "price", "prices", "pricing", "cost", "costs", "cheap", "cheapest", "discount", "coupon", "quote",
         "hire", "order", "subscribe", "trial", "demo", "for sale", "shop", "purchase", "best", "top", "vs",
         "versus", "review", "reviews", "alternative", "alternatives", "compare", "comparison", "software",
         "tool", "tools", "app", "platform", "service", "services", "agency", "company", "companies", "provider",
         "near me", "worth it", "certification"]
QUESTION = ["what", "how", "why", "when", "who", "where", "which", "guide", "tutorial", "examples", "ideas",
            "tips", "meaning", "definition", "template", "templates", "checklist", "agenda"]


def _rx(words):
    return re.compile(r"(?<![a-z0-9])(?:" + "|".join(re.escape(w) for w in sorted(words, key=len, reverse=True))
                      + r")(?![a-z0-9])")


BUYER_RX, QUESTION_RX = _rx(BUYER), _rx(QUESTION)


def word_count(keyword: str) -> int:
    return len(str(keyword).split())


def bucket(words: int) -> str:
    return "1-2 words" if words <= 2 else "3-6 words" if words <= 6 else "7+ words"


HOW_TO = re.compile(r"^(?:how to|what is|what are|why)\b")


def intent(keyword: str) -> str:
    kw = str(keyword).lower().strip()
    if HOW_TO.search(kw):  # "how to estimate project costs" is research, not a purchase
        return "research"
    if BUYER_RX.search(kw):
        return "buyer"
    if QUESTION_RX.search(kw):
        return "research"
    return "unclear"


def tier(words: int, kw_intent: str) -> str:
    if words >= 3 and kw_intent == "buyer":
        return "1 revenue priority"
    if words >= 3:
        return "2 long-tail support"
    if kw_intent == "buyer":
        return "3 head term, buyer"
    return "4 head term, awareness"


TIERS = ["1 revenue priority", "2 long-tail support", "3 head term, buyer", "4 head term, awareness"]
ACTION = {
    "1 revenue priority": "Build or improve a page for this exact need, with pricing context and a clear next step",
    "2 long-tail support": "Cover it as a section or supporting article linked to your money page",
    "3 head term, buyer": "Hard to win and converts low; target the longer variants first",
    "4 head term, awareness": "Awareness only; don't plan revenue on it",
}
COLUMNS = ["keyword", "words", "length", "volume", "intent", "conversion_rate_pct", "est_clicks",
           "est_conversions", "est_revenue", "revenue_score", "tier", "action"]


def load(path) -> pd.DataFrame:
    """CSV with a keyword column and a volume column (Ahrefs, Semrush, Keyword Planner, GSC)."""
    raw = pd.read_csv(path)
    kw = find_column(raw, ["keyword", "query", "top queries", "search term", "keywords"]) or raw.columns[0]
    vol = find_column(raw, ["volume", "search volume", "avg. monthly searches", "impressions"])
    df = pd.DataFrame({"keyword": raw[kw].astype(str).str.strip().str.lower(),
                       "volume": to_number(raw[vol]) if vol else 0.0})
    return df[df["keyword"] != ""].drop_duplicates("keyword").reset_index(drop=True)


def score(df: pd.DataFrame, ctr: float = 10.0, value: float = 100.0) -> pd.DataFrame:
    """ctr in percent (expected CTR if you rank), value = money per conversion."""
    rows = []
    for kw, vol in zip(df["keyword"], df["volume"]):
        n = word_count(kw)
        rate = CONV_RATE[min(max(n, 1), 7)]
        conv = vol * ctr / 100 * rate / 100
        it = intent(kw)
        t = tier(n, it)
        rows.append({"keyword": kw, "words": n, "length": bucket(n), "volume": int(vol), "intent": it,
                     "conversion_rate_pct": rate, "est_clicks": round(vol * ctr / 100, 1),
                     "est_conversions": round(conv, 2), "est_revenue": round(conv * value, 2),
                     "revenue_score": 0, "tier": t, "action": ACTION[t]})
    out = pd.DataFrame(rows, columns=COLUMNS)
    if out.empty:
        return out
    top = out["est_revenue"].max() or 1
    out["revenue_score"] = (out["est_revenue"] / top * 100).round().astype(int)
    return out.sort_values(["tier", "est_revenue"], ascending=[True, False]).reset_index(drop=True)


def summary(scored: pd.DataFrame) -> pd.DataFrame:
    vol_total = max(float(scored["volume"].sum()), 1.0)
    rev_total = float(scored["est_revenue"].sum())
    rows = []
    for b in BUCKETS:
        g = scored[scored["length"] == b]
        rev = float(g["est_revenue"].sum())
        rows.append({"length": b, "keywords": len(g), "volume": int(g["volume"].sum()),
                     "share_of_volume_pct": round(g["volume"].sum() / vol_total * 100, 1),
                     "est_revenue": round(rev, 2),
                     "share_of_est_revenue_pct": round(rev / rev_total * 100, 1) if rev_total else 0.0,
                     "np_digital_revenue_share": NP_REVENUE_SHARE[b]})
    return pd.DataFrame(rows)


def analyze(path, ctr=10.0, value=100.0):
    scored = score(load(path), ctr, value)
    return scored, summary(scored)
