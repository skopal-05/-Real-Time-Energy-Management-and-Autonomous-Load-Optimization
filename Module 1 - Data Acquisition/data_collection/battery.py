from __future__ import annotations

import random
from datetime import datetime

from synthetic_utils import bounded, build_rows, timestamp_series, write_csv


def generate_battery(periods: int = 96) -> str:
    start = datetime(2026, 7, 1, 0, 0)
    timestamps = timestamp_series(start, periods=periods, minutes=15)
    state_of_charge = 62.0

    def make_row(index: int, _timestamp: datetime) -> dict[str, object]:
        nonlocal state_of_charge
        power_kw = random.uniform(-75, 90)
        state_of_charge = bounded(state_of_charge + power_kw * 0.012, 15, 95)
        return {
            "state_of_charge_percent": round(state_of_charge, 2),
            "battery_power_kw": round(power_kw, 2),
            "voltage_v": round(690 + random.uniform(-8, 8), 2),
            "current_a": round(power_kw * 1000 / 690, 2),
            "temperature_c": round(30 + abs(power_kw) * 0.035 + random.uniform(-1.5, 1.5), 2),
            "mode": "charging" if power_kw > 0 else "discharging",
        }

    return str(write_csv("battery_storage.csv", build_rows("battery_storage_1", timestamps, make_row)))


if __name__ == "__main__":
    print(generate_battery())
