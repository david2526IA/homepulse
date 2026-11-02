from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class EnergyReading:
    timestamp: datetime
    kwh: float
    price_eur_kwh: float
