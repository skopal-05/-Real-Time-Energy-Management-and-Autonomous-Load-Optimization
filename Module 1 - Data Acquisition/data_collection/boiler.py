from __future__ import annotations

import random
from datetime import datetime

from synthetic_utils import build_rows, random_walk, timestamp_series, write_csv


def generate_boiler(periods: int = 96) -> str:
    start = datetime(2026, 7, 1, 0, 0)
    timestamps = timestamp_series(start, periods=periods, minutes=15)
    pressure_values = random_walk(8.2, periods, step=0.18, low=7.2, high=9.4)

    def make_row(index: int, _timestamp: datetime) -> dict[str, object]:
        pressure = pressure_values[index]
        steam_flow = round(random.uniform(1180, 1500) + pressure * 45, 2)
        return {
            "steam_pressure_bar": pressure,
            "steam_flow_kg_hr": steam_flow,
            "fuel_flow_m3_hr": round(82 + steam_flow * 0.035 + random.uniform(-2.5, 2.5), 2),
            "feedwater_temperature_c": round(random.uniform(78, 94), 2),
            "flue_gas_temperature_c": round(random.uniform(165, 215), 2),
            "efficiency_percent": round(random.uniform(78.5, 86.5), 2),
        }

    return str(write_csv("boiler.csv", build_rows("boiler_1", timestamps, make_row)))


if __name__ == "__main__":
    print(generate_boiler())
