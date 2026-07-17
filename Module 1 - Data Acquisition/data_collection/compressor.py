from __future__ import annotations

import random
from datetime import datetime

print("compressor.py is running...")

from synthetic_utils import (
    build_rows,
    daily_curve,
    timestamp_series,
    write_csv,
)


def generate_compressor(system_id: str = "air_compressor", periods: int = 96) -> str:
    start = datetime(2026, 7, 1, 0, 0)
    timestamps = timestamp_series(start, periods=periods, minutes=15)

    def make_row(index: int, _timestamp: datetime) -> dict[str, object]:
        load_factor = 0.30 + daily_curve(index, periods, peak=0.60)

        air_flow = round(random.uniform(80, 150) * load_factor, 2)
        power = round(random.uniform(40, 75) * load_factor, 2)

        return {
            "air_flow_m3_min": air_flow,
            "discharge_pressure_bar": round(
                random.uniform(6.5, 9.5) * load_factor, 2
            ),
            "power_consumption_kw": power,
            "motor_temperature_c": round(
                40 + power * 0.25 + random.uniform(-2, 2), 2
            ),
            "vibration_mm_s": round(
                random.uniform(0.8, 3.5) * load_factor, 3
            ),
            "status": "running" if air_flow > 30 else "idle",
        }

    filename = "air_compressor.csv"
    return str(write_csv(filename, build_rows(system_id, timestamps, make_row)))


if __name__ == "__main__":
    print("Generating compressor dataset...")
    result = generate_compressor()
    print("Dataset saved at:", result)