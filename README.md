# HomePulse

> Local-first household energy analytics with transparent forecasts and actionable usage insights.

[![CI](https://github.com/david2526IA/homepulse/actions/workflows/ci.yml/badge.svg)](https://github.com/david2526IA/homepulse/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Privacy](https://img.shields.io/badge/Privacy-local--first-0F766E)](#privacy-and-scope)
[![License](https://img.shields.io/badge/License-MIT-2563EB.svg)](LICENSE)

HomePulse turns a household energy CSV export into a clear local report: total consumption and estimated cost, hourly patterns, unusual spikes and a transparent next-day forecast. It is designed as a practical user-facing data product, not a black-box recommendation engine.

## Features

- Validate chronological consumption readings from a simple CSV contract.
- Identify average hourly patterns and atypical consumption spikes.
- Estimate cost from the price provided with each reading.
- Forecast each hour using its historical average — simple and auditable.
- Generate deterministic demo data, a JSON report and a local web interface.
- Optional FastAPI service, Docker image, tests and CI.

## Quick start

```bash
git clone https://github.com/david2526IA/homepulse.git
cd homepulse
python -m venv .venv
```

Activate the environment, then:

```bash
pip install -e ".[dev]"
homepulse demo --output data/demo_energy.csv
homepulse analyse data/demo_energy.csv --output artifacts/homepulse_report.json
pytest -q
```

## CSV contract

```csv
timestamp,kwh,price_eur_kwh
2026-01-01T00:00:00+00:00,0.28,0.17
```

Readings must be chronological, with non-negative energy and price values. `kwh` represents the energy consumed during each interval; keep the interval consistent throughout a file.

## Web app

```bash
pip install -e ".[web]"
uvicorn homepulse.api:app --reload
```

Open `http://127.0.0.1:8000`, upload a CSV and inspect the resulting report. For Docker:

```bash
docker build -t homepulse .
docker run --rm -p 8000:8000 homepulse
```

## Privacy and scope

The baseline processes the uploaded file only in the local process and does not require a cloud account. It is an educational analytics tool; it does not provide financial, electrical-installation or tariff advice. Validate meter exports and consult qualified professionals for safety or contractual decisions.

## Roadmap

- [ ] Smart-meter and Home Assistant adapters
- [ ] Tariff-aware scheduling simulation
- [ ] Accessible visual dashboard
- [ ] Solar-generation and battery scenarios
- [ ] Forecast accuracy tracking

## License

MIT © 2026 David
