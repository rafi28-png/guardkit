"""CLI: wattshift advise --max-delay-hours 4 --duration-minutes 60 --energy-kwh 2"""
import argparse
import json
import sys

from .badge import badge_svg
from .grid import fetch_forecast
from .optimizer import carbon_math, find_best_window


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="wattshift")
    sub = parser.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("advise", help="Find the cleanest window for a job")
    a.add_argument("--max-delay-hours", type=float, default=4, help="SLA: max hours you can wait")
    a.add_argument("--duration-minutes", type=int, default=60, help="How long the job runs")
    a.add_argument("--energy-kwh", type=float, default=1.0, help="Estimated energy for the job")
    a.add_argument("--forecast-file", help="JSON forecast file (for tests / offline demos)")
    a.add_argument("--now", help="ISO start time (for reproducible tests)")
    a.add_argument("--out", default="wattshift.json")
    a.add_argument("--report", default="wattshift.md")
    a.add_argument("--badge", default="wattshift-badge.svg")
    args = parser.parse_args(argv)

    if args.cmd == "advise":
        forecast, source = fetch_forecast(args.max_delay_hours, args.forecast_file)
        verdict = find_best_window(forecast, args.duration_minutes, args.max_delay_hours, args.now)
        carbon = carbon_math(verdict, args.energy_kwh)
        result = {"source": source, **verdict, **carbon,
                  "recommendation": (
                      f"Wait {verdict['delay_minutes']} min and start at {verdict['best_start']}"
                      if verdict["delay_minutes"] > 0 else
                      "Run now - now is already the cleanest window in your SLA"
                  )}
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        md = "\n".join([
            "# WattShift Advice",
            "",
            f"**Source:** {source}",
            f"**Recommendation:** {result['recommendation']}",
            "",
            "| | Start | Avg intensity (gCO2/kWh) | CO2 (kg) |",
            "|---|---|---|---|",
            f"| Run now | {verdict['immediate_start']} | {verdict['immediate_intensity']} | {carbon['immediate_co2_kg']} |",
            f"| Best in SLA | {verdict['best_start']} | {verdict['best_intensity']} | {carbon['best_co2_kg']} |",
            "",
            f"**Saved:** {carbon['saved_co2_g']} g CO2 ({carbon['saved_pct']}%) for {args.energy_kwh} kWh",
            "",
        ])
        with open(args.report, "w", encoding="utf-8") as f:
            f.write(md)
        with open(args.badge, "w", encoding="utf-8") as f:
            f.write(badge_svg(carbon["saved_co2_g"], carbon["saved_pct"]))
        print(md)
        print(f"Wrote {args.out}, {args.report}, {args.badge}")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
