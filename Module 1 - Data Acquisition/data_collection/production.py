from __future__ import annotations

import random
from datetime import datetime

from synthetic_utils import build_rows, daily_curve, timestamp_series, write_csv


def generate_production_line(line_id: str, periods: int = 96) -> str:
    start = datetime(2026, 7, 1, 0, 0)
    timestamps = timestamp_series(start, periods=periods, minutes=15)

    def make_row(index: int, _timestamp: datetime) -> dict[str, object]:
        load_factor = 0.35 + daily_curve(index, periods, peak=0.55)
        units_per_hour = round(random.uniform(80, 115) * load_factor, 2)
        machine_load_kw = round(random.uniform(95, 135) * load_factor, 2)
        return {
            "units_per_hour": units_per_hour,
            "machine_load_kw": machine_load_kw,
            "motor_temperature_c": round(42 + machine_load_kw * 0.09 + random.uniform(-1.5, 1.5), 2),
            "vibration_mm_s": round(random.uniform(1.0, 3.8) * load_factor, 3),
            "status": "running" if units_per_hour > 25 else "idle",
        }

    filename = f"{line_id.lower()}_production.csv"
    return str(write_csv(filename, build_rows(line_id, timestamps, make_row)))


if __name__ == "__main__":
    for system in ("production_line_a", "production_line_b"):
        print(generate_production_line(system))
