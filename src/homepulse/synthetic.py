from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path


def generate(path: str | Path, days: int = 14, seed: int = 17) -> None:
    randomizer = random.Random(seed)
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    with Path(path).open("w", newline="", encoding="utf-8") as destination:
        writer = csv.DictWriter(destination, fieldnames=["timestamp", "kwh", "price_eur_kwh"])
        writer.writeheader()
        for offset in range(days * 24):
            moment = start + timedelta(hours=offset)
            evening_peak = 0.85 if 18 <= moment.hour <= 22 else 0.0
            price = 0.17 + (0.11 if 19 <= moment.hour <= 22 else 0.0)
            spike = 2.2 if offset == 121 else 0.0
            writer.writerow({
                "timestamp": moment.isoformat(),
                "kwh": round(0.28 + evening_peak + spike + randomizer.uniform(-0.06, 0.06), 3),
                "price_eur_kwh": round(price, 3),
            })
