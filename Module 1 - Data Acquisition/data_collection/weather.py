from __future__ import annotations

import random
from datetime import datetime

from synthetic_utils import build_rows, daily_curve, timestamp_series, write_csv


def generate_weather(periods: int = 96) -> str:
    start = datetime(2026, 7, 1, 0, 0)
    timestamps = timestamp_series(start, periods=periods, minutes=15)

    def make_row(index: int, _timestamp: datetime) -> dict[str, object]:
        sun = daily_curve(index, periods)
        return {
            "ambient_temperature_c": round(25 + sun * 9 + random.uniform(-1.8, 1.8), 2),
            "humidity_percent": round(70 - sun * 22 + random.uniform(-4, 4), 2),
            "wind_speed_m_s": round(random.uniform(1.5, 6.5), 2),
            "cloud_cover_percent": round(random.uniform(10, 75), 2),
            "global_irradiance_w_m2": round(max(0, sun * 920 + random.uniform(-45, 45)), 2),
        }

    return str(write_csv("weather.csv", build_rows("weather_station_1", timestamps, make_row)))


if __name__ == "__main__":
    print(generate_weather())
