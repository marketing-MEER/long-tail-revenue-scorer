"""Command line entry point: `long-tail-revenue-scorer KEYWORDS.csv`."""
from pathlib import Path

import click

from . import __version__, core
from .benchmark import STATS
from .report import Report, write_excel


@click.command()
@click.argument("keywords_file", type=click.Path(exists=True))
@click.option("--ctr", default=10.0, show_default=True, help="Expected click-through rate in percent if you rank.")
@click.option("--value", default=100.0, show_default=True, help="Money per conversion (order value or lead value).")
@click.option("-o", "--output", default="long_tail_revenue", show_default=True,
              help="Report name; writes <name>.html and <name>.xlsx")
@click.version_option(__version__)
def main(keywords_file, ctr, value, output):
    """Score every keyword in KEYWORDS_FILE (CSV with keyword + volume) by revenue potential.

    Built by Meer Hamza - linkedin.com/in/meerhamza-seo
    """
    scored, summ = core.analyze(keywords_file, ctr, value)
    t = scored["tier"].value_counts()
    report = Report(title="Long-tail revenue report",
                    subtitle=f"{Path(keywords_file).name} · {len(scored):,} keywords · CTR {ctr:g}% · "
                             f"value {value:g} per conversion", tool="long-tail-revenue-scorer")
    report.add_cards([
        ("Keywords", len(scored)),
        ("Revenue priority", int(t.get(core.TIERS[0], 0)), "good"),
        ("Long-tail support", int(t.get(core.TIERS[1], 0))),
        ("Head terms", int(t.get(core.TIERS[2], 0) + t.get(core.TIERS[3], 0)), "warn"),
        ("Est. conversions / month", round(float(scored["est_conversions"].sum()), 1)),
        ("Est. revenue / month", round(float(scored["est_revenue"].sum()), 2)),
    ])
    report.add_benchmark(STATS[1], how_used="Each keyword's conversion rate is NP Digital's rate for its word "
                         "count (7+ words use the seven-plus rate). Estimated revenue = volume x your CTR x that "
                         "rate x your value per conversion.")
    report.add_benchmark(STATS[0], how_used="The summary puts your list's estimated revenue split by length next "
                         "to NP Digital's measured split, so you can see if your plan leans on short head terms.")
    report.add_table("Revenue by keyword length", summ, sheet="Summary",
                     note="Estimates use your CTR and value inputs. The last column is NP Digital's measured share.")
    for name in core.TIERS:
        g = scored[scored["tier"] == name].drop(columns=["tier", "action"])
        report.add_table(name[2:].capitalize(), g, note=core.ACTION[name], sheet=name[2:].capitalize())
    report.add_table("All keywords", scored, sheet="All keywords")

    html_path = report.save_html(Path(output).with_suffix(".html"))
    xlsx_path = write_excel(report.sheets, Path(output).with_suffix(".xlsx"))
    click.secho(f"Report: {html_path}\nData:   {xlsx_path}", fg="green", bold=True)
    click.echo(summ[["length", "keywords", "volume", "share_of_est_revenue_pct"]].to_string(index=False))


if __name__ == "__main__":
    main()
