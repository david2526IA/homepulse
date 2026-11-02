"""Dependency-free consumption analytics with transparent recommendations."""

from __future__ import annotations

from collections import defaultdict
from statistics import mean, median

from .models import EnergyReading


def analyse(readings: list[EnergyReading]) -> dict[str, object]:
    if not readings:
        raise ValueError("At least one energy reading is required")
    values = [item.kwh for item in readings]
    total_kwh = sum(values)
    total_cost = sum(item.kwh * item.price_eur_kwh for item in readings)
    hourly: dict[int, list[EnergyReading]] = defaultdict(list)
    for item in readings:
        hourly[item.timestamp.hour].append(item)
    by_hour = {
        hour: round(mean(item.kwh for item in items), 4)
        for hour, items in sorted(hourly.items())
    }
    peak_hour = max(by_hour, key=by_hour.get)
    baseline = median(values)
    spikes = [item for item in readings if item.kwh > baseline * 2.25 and item.kwh > 0.2]
    cheapest_hour = min(by_hour, key=by_hour.get)
    recommendations = [
        f"Your average consumption peak is around {peak_hour:02d}:00 ({by_hour[peak_hour]:.2f} kWh/hour).",
        f"The lowest average-consumption hour is {cheapest_hour:02d}:00 ({by_hour[cheapest_hour]:.2f} kWh/hour).",
    ]
    if spikes:
        recommendations.append(f"Review {len(spikes)} unusual consumption spike(s); compare them with appliance usage.")
    return {
        "readings": len(readings),
        "total_kwh": round(total_kwh, 3),
        "estimated_cost_eur": round(total_cost, 2),
        "average_kwh_per_reading": round(mean(values), 4),
        "peak_hour": peak_hour,
        "hourly_average_kwh": by_hour,
        "spikes": [{"timestamp": item.timestamp.isoformat(), "kwh": item.kwh} for item in spikes],
        "recommendations": recommendations,
    }


def forecast_next_day(readings: list[EnergyReading]) -> list[dict[str, float | int]]:
    """Forecast each hour from its historical average; transparent over opaque."""
    buckets: dict[int, list[float]] = defaultdict(list)
    for item in readings:
        buckets[item.timestamp.hour].append(item.kwh)
    return [
        {"hour": hour, "forecast_kwh": round(mean(buckets[hour]), 4)}
        for hour in sorted(buckets)
    ]
