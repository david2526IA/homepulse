from __future__ import annotations

import argparse
import json
from pathlib import Path

from .analytics import analyse, forecast_next_day
from .io import load_readings
from .synthetic import generate


def main() -> None:
    parser = argparse.ArgumentParser(prog="homepulse")
    commands = parser.add_subparsers(dest="command", required=True)
    demo = commands.add_parser("demo", help="generate deterministic household energy data")
    demo.add_argument("--output", default="data/demo_energy.csv")
    analyse_command = commands.add_parser("analyse", help="create a local energy report")
    analyse_command.add_argument("input")
    analyse_command.add_argument("--output", default="artifacts/homepulse_report.json")
    args = parser.parse_args()
    if args.command == "demo":
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        generate(args.output)
        print(f"Demo energy data written to {args.output}")
        return
    readings = load_readings(args.input)
    report = {"analysis": analyse(readings), "next_day_forecast": forecast_next_day(readings)}
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Analysed {len(readings)} readings. Report written to {output}")


if __name__ == "__main__":
    main()
