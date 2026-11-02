from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

from .models import EnergyReading


def load_readings(path: str | Path) -> list[EnergyReading]:
    with Path(path).open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        required = {"timestamp", "kwh", "price_eur_kwh"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")
        records = []
        previous = None
        for line, row in enumerate(reader, start=2):
            try:
                reading = EnergyReading(
                    datetime.fromisoformat(row["timestamp"]), float(row["kwh"]), float(row["price_eur_kwh"])
                )
            except ValueError as error:
                raise ValueError(f"Invalid data at line {line}: {error}") from error
            if reading.kwh < 0 or reading.price_eur_kwh < 0:
                raise ValueError(f"Negative energy or price at line {line}")
            if previous is not None and reading.timestamp <= previous:
                raise ValueError(f"Timestamps must be strictly increasing (line {line})")
            previous = reading.timestamp
            records.append(reading)
    return records
