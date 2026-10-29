"""Pick the cleanest execution window inside an SLA delay."""
from datetime import datetime


def _parse(t: str) -> datetime:
    return datetime.fromisoformat(t.replace("Z", "+00:00"))


def find_best_window(forecast, duration_minutes: int, max_delay_hours: int, now_iso: str | None = None):
    """Sliding-window average intensity. Returns a dict with the verdict."""
    if not forecast:
        raise ValueError("Empty forecast")
    slots = sorted(forecast, key=lambda x: x["time"])
    # Slot length in minutes, inferred from the first two slots (default 30)
    slot_min = 30
    if len(slots) >= 2:
        slot_min = max(1, int((_parse(slots[1]["time"]) - _parse(slots[0]["time"])).total_seconds() // 60))
    need = max(1, duration_minutes // slot_min)
    now = _parse(now_iso) if now_iso else _parse(slots[0]["time"])
    # Only windows that start within the allowed delay
    candidates = []
    for i in range(len(slots) - need + 1):
        start = _parse(slots[i]["time"])
        if (start - now).total_seconds() < 0:
            continue
        if (start - now).total_seconds() > max_delay_hours * 3600:
            break
        window = slots[i:i + need]
        avg = sum(s["intensity_gco2_kwh"] for s in window) / len(window)
        candidates.append((avg, slots[i]["time"], window))
    if not candidates:
        raise ValueError("No window fits inside the max delay")
    immediate_avg = candidates[0][0]
    best_avg, best_start, best_window = min(candidates, key=lambda x: x[0])
    return {
        "immediate_start": candidates[0][1],
        "immediate_intensity": round(immediate_avg, 1),
        "best_start": best_start,
        "best_intensity": round(best_avg, 1),
        "best_end": best_window[-1]["time"],
        "delay_minutes": int((_parse(best_start) - now).total_seconds() // 60),
        "slots_checked": len(candidates),
    }


def carbon_math(verdict: dict, energy_kwh: float) -> dict:
    immediate_kg = energy_kwh * verdict["immediate_intensity"] / 1000
    best_kg = energy_kwh * verdict["best_intensity"] / 1000
    saved_kg = immediate_kg - best_kg
    saved_pct = (saved_kg / immediate_kg * 100) if immediate_kg else 0
    return {
        "energy_kwh": energy_kwh,
        "immediate_co2_kg": round(immediate_kg, 4),
        "best_co2_kg": round(best_kg, 4),
        "saved_co2_kg": round(saved_kg, 4),
        "saved_co2_g": round(saved_kg * 1000, 1),
        "saved_pct": round(saved_pct, 1),
    }
