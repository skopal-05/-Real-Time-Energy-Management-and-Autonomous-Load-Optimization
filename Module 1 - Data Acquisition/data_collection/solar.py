from __future__ import annotations

import random
from datetime import datetime

from synthetic_utils import build_rows, daily_curve, timestamp_series, write_csv


def generate_solar(periods: int = 96) -> str:
    start = datetime(2026, 7, 1, 0, 0)
    timestamps = timestamp_series(start, periods=periods, minutes=15)

    def make_row(index: int, _timestamp: datetime) -> dict[str, object]:
        sun = daily_curve(index, periods, peak=1.0)
        irradiance = round(max(0, 950 * sun + random.uniform(-35, 35)), 2)
        power_kw = round(irradiance * 0.42 + random.uniform(-8, 8), 2)
        return {
            "irradiance_w_m2": irradiance,
            "dc_power_kw": max(0, power_kw),
            "inverter_power_kw": max(0, round(power_kw * random.uniform(0.94, 0.98), 2)),
            "panel_temperature_c": round(28 + sun * 22 + random.uniform(-2, 2), 2),
            "inverter_status": "online" if irradiance > 25 else "standby",
        }

    return str(write_csv("solar_plant.csv", build_rows("solar_plant_1", timestamps, make_row)))


if __name__ == "__main__":
    print(generate_solar())
