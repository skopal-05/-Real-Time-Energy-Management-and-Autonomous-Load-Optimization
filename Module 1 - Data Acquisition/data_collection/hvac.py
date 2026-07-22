from __future__ import annotations

import random
from datetime import datetime

print("hvac.py is running...")

from synthetic_utils import (
    build_rows,
    daily_curve,
    timestamp_series,
    write_csv,
)


def generate_hvac(system_id: str = "hvac", periods: int = 96) -> str:
    start = datetime(2026, 7, 1, 0, 0)
    timestamps = timestamp_series(start, periods=periods, minutes=15)

    def make_row(index: int, _timestamp: datetime) -> dict[str, object]:
        load_factor = 0.30 + daily_curve(index, periods, peak=0.60)

        power = round(random.uniform(15, 25) * load_factor, 2)
        airflow = round(random.uniform(800, 2000) * load_factor, 2)

        return {
            "power_kw": power,
            "temperature_c": round(
                random.uniform(20, 28) + random.uniform(-1.5, 1.5), 2
            ),
            "airflow_m3_min": airflow,
            "humidity_percent": round(
                random.uniform(40, 65), 2
            ),
            "setpoint_temperature_c": random.choice([22, 23, 24]),
            "efficiency_percent": round(
                random.uniform(85, 98), 2
            ),
            "status": "running" if power > 5 else "idle",
        }

    filename = "hvac.csv"
    return str(write_csv(filename, build_rows(system_id, timestamps, make_row)))


if __name__ == "__main__":
    print("Generating HVAC dataset...")
    result = generate_hvac()
    print("Dataset saved at:", result)