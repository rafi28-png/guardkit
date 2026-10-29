"""Grid carbon-intensity forecasts.

Primary source: UK National Grid Carbon Intensity API (free, no key):
  https://api.carbonintensity.org.uk/intensity/{from}/fw24h
It returns half-hourly forecast intensity in gCO2/kWh.

If that API is unreachable (offline, non-UK, rate-limited), we fall
back to a clearly-labelled synthetic forecast so the tool still
works and can be demoed. The source is always reported, never hidden.
"""
import json
import math
import urllib.request
from datetime import datetime, timedelta, timezone


def _demo_forecast(hours: int = 24) -> list:
    """Synthetic, plausible pattern: low overnight, higher at evening peak."""
    now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    out = []
    for i in range(hours * 2):  # half-hour slots
        t = now + timedelta(minutes=30 * i)
        # Peak around 18:00, trough around 03:00
        intensity = 180 + 120 * math.sin((t.hour + t.minute / 60 - 9) / 24 * 2 * math.pi)
        out.append({"time": t.isoformat(), "intensity_gco2_kwh": round(max(40, intensity))})
    return out


def fetch_forecast(max_delay_hours: int = 4, forecast_file: str | None = None):
    """Return (forecast_list, source_name)."""
    if forecast_file:
        data = json.loads(open(forecast_file, encoding="utf-8").read())
        # Accept either a list or {"forecast": [...]}
        if isinstance(data, dict):
            data = data.get("forecast", [])
        return data, f"file:{forecast_file}"

    # Try the free UK API for the next 24h
    try:
        now = datetime.now(timezone.utc)
        start = now.strftime("%Y-%m-%dT%H:%MZ")
        url = f"https://api.carbonintensity.org.uk/intensity/{start}/fw24h"
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            payload = json.loads(resp.read())
        forecast = []
        for item in payload.get("data", []):
            forecast.append({
                "time": item["from"],
                "intensity_gco2_kwh": item["intensity"]["forecast"],
            })
        if forecast:
            return forecast, "api.carbonintensity.org.uk (UK, free, no key)"
    except Exception:
        pass
    return _demo_forecast(24), "demo-fallback (offline / non-UK - synthetic, for demo only)"
