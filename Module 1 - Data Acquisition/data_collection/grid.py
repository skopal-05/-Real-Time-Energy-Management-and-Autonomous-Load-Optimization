from __future__ import annotations

import random
from datetime import datetime

from synthetic_utils import build_rows, daily_curve, timestamp_series, write_csv


def generate_grid(periods: int = 96) -> str:
    start = datetime(2026, 7, 1, 0, 0)
    timestamps = timestamp_series(start, periods=periods, minutes=15)

    def make_row(index: int, _timestamp: datetime) -> dict[str, object]:
        demand_shape = 0.6 + daily_curve(index, periods, peak=0.35)
        import_power = round(random.uniform(380, 620) * demand_shape, 2)
        return {
            "grid_import_kw": import_power,
            "grid_export_kw": round(max(0, random.uniform(-20, 65) * daily_curve(index, periods)), 2),
            "frequency_hz": round(random.uniform(49.86, 50.08), 3),
            "voltage_v": round(random.uniform(410, 424), 2),
            "power_factor": round(random.uniform(0.88, 0.99), 3),
            "tariff_inr_kwh": round(random.choice([6.5, 7.2, 8.1, 9.4]), 2),
        }

    return str(write_csv("grid.csv", build_rows("grid_connection_1", timestamps, make_row)))


if __name__ == "__main__":
    print(generate_grid())
