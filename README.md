<div align="center">

# 💰 long-tail-revenue-scorer

### Score any keyword list by revenue potential, using keyword length, buyer intent and NP Digital's conversion data.

[![tests](https://github.com/marketing-MEER/long-tail-revenue-scorer/actions/workflows/ci.yml/badge.svg)](https://github.com/marketing-MEER/long-tail-revenue-scorer/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white)
![License: MIT](https://img.shields.io/badge/license-MIT-green)
![No API keys](https://img.shields.io/badge/API%20keys-none%20needed-brightgreen)
[![Part of SEO Toolbox](https://img.shields.io/badge/part%20of-SEO%20Toolbox-orange)](https://github.com/marketing-MEER/seo-toolbox)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Meer%20Hamza-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/meerhamza-seo)

[🚀 Quick start](#quick-start) · [⚙️ How it works](#how-it-works) · [📄 Report](#report) · [❓ FAQ](#faq) · [👤 Author](#author)

</div>

---

## 💡 What it does

Most keyword lists get sorted by search volume, so the plan fills up with short head terms that are hard to rank for and rarely turn into sales.

`long-tail-revenue-scorer` reads any keyword CSV with volume and gives every keyword a conversion rate based on its length, an estimated number of conversions and revenue, a 0-100 revenue score and a tier that says what to do with it.

- ✅ Conversion rate per keyword length from NP Digital's measured data (1 to 7+ words)
- ✅ Buyer, research or unclear intent tag, and four tiers: revenue priority, long-tail support, buyer head term, awareness head term
- ✅ Your list's revenue split by length, side by side with NP Digital's measured split
- ✅ Free, MIT licensed, no API keys. Works with the exports you already have.

## 📊 Why this matters

> **Conversion Rate by Keyword Length: Long-Tail Keywords Win** · NP Digital, May 2025 (40 companies, paid search, branded terms excluded)
> - One-word keywords convert at 0.17%.
> - Two-word keywords convert at 0.35%.
> - Three-word queries jump to 1.02%.
> - Six-word keywords peak at 1.94%.
>
> **Which Keyword Lengths Drive Revenue** · NP Digital, August 2025 (1,048,552 leads across four years)
> - 1 to 2 word keywords drove under 6 percent revenue.
> - 3 to 6 words drove around 45 percent.
> - 7 plus words exceeded 50 percent by 2025.
>
> Data: [conversion rate by length](https://neilpatel.com/marketing-stats/conversion-rate-by-keyword-length/) · [revenue by length](https://neilpatel.com/marketing-stats/keyword-length-revenue-impact/) · [organic traffic by length](https://neilpatel.com/marketing-stats/organic-traffic-by-keyword-length/)

**How long-tail-revenue-scorer uses this:** the insight is *"measure keyword success by revenue, not traffic alone"*, so each keyword gets NP Digital's conversion rate for its word count and is scored on estimated revenue instead of volume. Head terms of one or two words go into their own tiers, following *"stop obsessing over single-word head terms"*.

<a id="quick-start"></a>

## 🚀 Quick start

```bash
git clone https://github.com/marketing-MEER/long-tail-revenue-scorer.git
cd long-tail-revenue-scorer
pip install -e .
long-tail-revenue-scorer examples/project_keywords.csv --ctr 10 --value 120
```

This writes **`long_tail_revenue.html`** (a formatted report you can open, share or print to PDF) and **`long_tail_revenue.xlsx`** (all the data, one sheet per tier).

> [!TIP]
> If the `long-tail-revenue-scorer` command isn't found, use `python -m long_tail_revenue_scorer`.

## 📥 Input

| Input | Notes |
|---|---|
| Any keyword CSV | The keyword column is found by name (`Keyword`, `Query`, `Top queries`, `Search term`), else the first column is used |
| Volume | `Volume`, `Search Volume`, `Avg. monthly searches` or `Impressions` |

Works with Ahrefs, Semrush, Google Keyword Planner and Search Console exports (Performance → Queries → Export, then impressions stand in for volume).

<a id="how-it-works"></a>

## ⚙️ How it works

1. **Count the words** in each keyword and look up NP Digital's conversion rate for that length: 1 word 0.17%, 2 words 0.35%, 3 words 1.02%, 4 words 1.61%, 5 words 1.58%, 6 words 1.94%, 7+ words 1.83%.
2. **Estimate**: clicks = volume x `--ctr`; conversions = clicks x conversion rate; revenue = conversions x `--value`. The revenue score is each keyword's revenue as a share of the best one (0-100).
3. **Tag intent**: *buyer* if the keyword has a choosing or buying word (best, vs, pricing, cost, alternatives, software, tool, agency, ...); *research* if it starts with how to / what is / why or has guide, template, examples; else *unclear*.
4. **Tier** each keyword:

| Tier | Rule | What to do |
|---|---|---|
| 1 revenue priority | 3+ words and buyer intent | Build or improve a page for this exact need, with pricing context and a clear next step |
| 2 long-tail support | 3+ words, research or unclear | Cover it as a section or supporting article linked to your money page |
| 3 head term, buyer | 1-2 words, buyer intent | Hard to win and converts low; target the longer variants first |
| 4 head term, awareness | 1-2 words, no buyer word | Awareness only; don't plan revenue on it |

### Options

| Option | Default | What it does |
|---|---|---|
| `--ctr` | `10` | Expected click-through rate in percent if you rank |
| `--value` | `100` | Money per conversion (average order value or lead value) |
| `-o`, `--output` | `long_tail_revenue` | File name for the report (`.html` + `.xlsx`) |

<a id="report"></a>

## 📄 The report

| Section / Excel sheet | Shows |
|---|---|
| Summary cards | Keywords per tier, estimated conversions and revenue per month |
| Benchmark panels | The two NP Digital stats behind the conversion rates and the length split |
| **Summary** | Keywords, volume and estimated revenue per length bucket, next to NP Digital's measured revenue share |
| **One sheet per tier** | Keyword, words, volume, intent, conversion rate, estimated clicks, conversions, revenue and score |
| **All keywords** | Everything, plus the action for each tier |

<details>
<summary>📄 Example: real output from <code>examples/</code> (fictional project-management keywords, CTR 10%, value 120)</summary>

**Revenue by keyword length**

| length | keywords | volume | share of volume pct | est revenue | share of est revenue pct | np digital revenue share |
|---|---|---|---|---|---|---|
| 1-2 words | 6 | 198,190 | 85.2 | 6369.18 | 55.1 | under 6% |
| 3-6 words | 11 | 29,830 | 12.8 | 4179.92 | 36.2 | around 45% |
| 7+ words | 3 | 4,590 | 2 | 1007.96 | 8.7 | over 50% by 2025 |

**Sample rows**

| keyword | words | volume | intent | conversion rate pct | est revenue | revenue score | tier |
|---|---|---|---|---|---|---|---|
| project management software | 3 | 22,200 | buyer | 1.02 | 2717.28 | 100 | 1 revenue priority |
| best project management software for small teams | 7 | 1,300 | buyer | 1.83 | 285.48 | 11 | 1 revenue priority |
| project management tool pricing | 4 | 880 | buyer | 1.61 | 170.02 | 6 | 1 revenue priority |
| how to make a gantt chart in excel | 8 | 2,900 | research | 1.83 | 636.84 | 23 | 2 long-tail support |
| planlane alternatives | 2 | 390 | buyer | 0.35 | 16.38 | 1 | 3 head term, buyer |
| project management | 2 | 49,500 | unclear | 0.35 | 2,079 | 77 | 4 head term, awareness |
| agile | 1 | 90,500 | unclear | 0.17 | 1846.2 | 68 | 4 head term, awareness |

This sample list is 85% head-term volume, so even at their low conversion rates the head terms carry 55% of the estimated revenue. NP Digital measured under 6% for them, because in practice a site rarely gets a 10% CTR on a term like "agile". That gap is the reason head terms get their own tiers.

</details>

## 🧰 More free SEO tools

This repo is one tool in the **[SEO Toolbox](https://github.com/marketing-MEER/seo-toolbox)**, a family of free, single-purpose SEO tools. Related:
- [keyword-intent-classifier](https://github.com/marketing-MEER/keyword-intent-classifier): tag any keyword list by search intent, with the reason shown
- [keyword-gap-analyzer](https://github.com/marketing-MEER/keyword-gap-analyzer): keywords competitors win and you don't
- [topic-cluster-planner](https://github.com/marketing-MEER/topic-cluster-planner): turn a keyword list into pillar and spoke pages
- [seo-workhorse](https://github.com/marketing-MEER/seo-workhorse): audit, clustering, redirects and GSC quick wins in one CLI

<a id="faq"></a>

## ❓ FAQ

<details><summary><b>Are the revenue numbers a forecast?</b></summary>

No. They use one CTR for every keyword and NP Digital's average conversion rates, so they are good for ranking a list against itself, not for a budget. Set `--ctr` lower for hard head terms by running them as a separate file if you want a closer estimate.
</details>

<details><summary><b>The conversion rates come from paid search. Do they apply to SEO?</b></summary>

They are the closest public numbers by keyword length, and NP Digital's separate study of 1 million leads shows the same pattern for revenue (long keywords win). Treat them as relative weights, not your site's real rates.
</details>

<details><summary><b>Is my data sent anywhere?</b></summary>

No. It reads your CSV and writes the report on your computer. It makes no network requests.
</details>

## 🧪 Tests

```bash
python -m unittest discover -s tests -t . -v
```

## 📄 License

[MIT](LICENSE). Free for personal and commercial use. Benchmark figures © their original publishers and quoted with a link to the source.

<a id="author"></a>

## 👤 Author

**Meer Hamza** · SEO Team Lead · Berlin 🇩🇪
10+ years in SEO, AEO and GEO. I build small tools that take the spreadsheet work out of SEO.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/meerhamza-seo)
[![Email](https://img.shields.io/badge/Email-meerhamza5%40gmail.com-D14836?logo=gmail&logoColor=white)](mailto:meerhamza5@gmail.com)

<div align="center">

**If this saved you time, a ⭐ helps other SEOs find it.**

</div>
