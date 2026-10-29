# WattShift

**Don't run a heavy batch job at the dirtiest, most expensive moment just because it was triggered then.**

Every day, test suites, cron jobs, and training runs start the second they are triggered — even if the grid is at peak coal/gas intensity. WattShift finds a cleaner window inside the deadline you set, and tells you exactly how much CO2 and money that saves.

This MVP is deliberately an *advisor*, not a blocker: it recommends a window, it doesn't force-delay your CI. That makes it adoptable without annoying developers.

## Demo (reproducible, no API needed)

```bash
python -m wattshift advise \
  --max-delay-hours 4 --duration-minutes 60 --energy-kwh 2 \
  --forecast-file examples/forecast.json \
  --now 2026-10-30T00:00:00+00:00
```

Real output from this project:

```
Recommendation: Wait 60 min and start at 2026-10-30T01:00:00+00:00

| | Start | Avg intensity (gCO2/kWh) | CO2 (kg) |
| Run now | 2026-10-30T00:00:00+00:00 | 290.0 | 0.58 |
| Best in SLA | 2026-10-30T01:00:00+00:00 | 115.0 | 0.23 |

Saved: 350.0 g CO2 (60.3%) for 2.0 kWh
```

## Live demo (free UK API, no key)

Running without `--forecast-file` queries the UK National Grid Carbon Intensity API. On the test run for this project it found:

```
Run now: 219.0 gCO2/kWh -> 0.219 kg
Best in 4h SLA: 146.0 gCO2/kWh -> 0.146 kg
Saved: 73.0 g CO2 (33.3%) for 1.0 kWh, by waiting 240 min
```

If the API is unreachable, it falls back to a clearly-labelled synthetic forecast — the source is always printed, never hidden.

## What you get

- `wattshift.json` — machine-readable advice (best start, intensities, savings)
- `wattshift.md` — a summary table you can append to a PR or GitHub Step Summary
- `wattshift-badge.svg` — a README badge, e.g. "🌱 CO2 saved 350g (60%)"

## Use it in GitHub Actions

See `.github/workflows/wattshift.yml`. It runs WattShift for nightly batch jobs and appends the advice to the workflow summary. Add it to a repo in a few lines — that's the viral loop.

## How it works

1. Fetch a half-hourly carbon-intensity forecast (UK API, or a file you supply)
2. Slide a window the length of your job across every start time inside your max delay
3. Pick the lowest average intensity, compare it with running now, and compute CO2 saved
4. Never claim precision it doesn't have: savings are estimates based on the forecast and the energy figure you give it

## Honest scope of this MVP

- Grid data: UK API only for live data; other regions need a provider (Electricity Maps / WattTime) in v2
- No CRIU checkpointing, no spot-price routing, no automatic region switching yet — those are v2, and they are much harder than the advisor
- Energy (kWh) is an input you estimate; the tool does not measure your job's real power draw

## Layout

```
wattshift/
  grid.py       # UK API + labelled demo fallback
  optimizer.py  # sliding-window best-time search + CO2 math
  badge.py      # SVG badge generator
  cli.py        # wattshift advise
examples/forecast.json
tests/test_wattshift.py
.github/workflows/wattshift.yml
```

## License

MIT
