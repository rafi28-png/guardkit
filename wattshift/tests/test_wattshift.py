import json
from pathlib import Path
from wattshift.optimizer import find_best_window, carbon_math

FORECAST = json.loads((Path(__file__).parent.parent / "examples" / "forecast.json").read_text())


def test_picks_cleanest_window_inside_sla():
    v = find_best_window(FORECAST, duration_minutes=60, max_delay_hours=4,
                         now_iso="2026-10-30T00:00:00+00:00")
    # 01:00 window averages (120+110)/2 = 115, cleaner than 00:00 (290)
    assert v["best_start"] == "2026-10-30T01:00:00+00:00"
    assert v["best_intensity"] == 115.0
    assert v["delay_minutes"] == 60


def test_savings_math():
    v = find_best_window(FORECAST, 60, 4, "2026-10-30T00:00:00+00:00")
    c = carbon_math(v, energy_kwh=2.0)
    # immediate 290 g/kWh * 2 = 580g, best 115 * 2 = 230g, saved 350g
    assert c["saved_co2_g"] == 350.0
    assert c["saved_pct"] > 50
