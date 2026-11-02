from datetime import datetime, timedelta, timezone

from homepulse.analytics import analyse, forecast_next_day
from homepulse.models import EnergyReading
from homepulse.synthetic import generate
from homepulse.io import load_readings


def test_analysis_finds_peak_and_spike() -> None:
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    readings = [EnergyReading(start + timedelta(hours=hour), 0.2, 0.2) for hour in range(23)]
    readings.append(EnergyReading(start + timedelta(hours=23), 1.5, 0.3))
    report = analyse(readings)
    assert report["peak_hour"] == 23
    assert len(report["spikes"]) == 1


def test_forecast_groups_by_hour() -> None:
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    readings = [EnergyReading(start, 1.0, 0.2), EnergyReading(start + timedelta(days=1), 3.0, 0.2)]
    assert forecast_next_day(readings) == [{"hour": 0, "forecast_kwh": 2.0}]


def test_generated_data_is_loadable(tmp_path) -> None:
    path = tmp_path / "energy.csv"
    generate(path, days=2)
    assert len(load_readings(path)) == 48
