from __future__ import annotations

import csv
import math
from datetime import datetime, timedelta
from pathlib import Path


# Folder where generated CSVs will be stored
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def timestamp_series(start: datetime, periods: int, minutes: int = 15):
    """
    Generate timestamps at a fixed interval.

    Example:
    2026-07-01 00:00
    2026-07-01 00:15
    2026-07-01 00:30
    ...
    """
    return [
        start + timedelta(minutes=i * minutes)
        for i in range(periods)
    ]


def daily_curve(index: int, periods: int, peak: float = 0.5):
    """
    Creates a smooth daily usage pattern using a sine wave.

    Returns values between 0 and peak.
    """
    angle = (2 * math.pi * index) / periods
    return peak * (math.sin(angle - math.pi / 2) + 1) / 2


def build_rows(system_id: str, timestamps, make_row):
    """
    Build a list of dictionaries by combining
    timestamps with sensor values.
    """

    rows = []

    for index, timestamp in enumerate(timestamps):
        row = {
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "system_id": system_id,
        }

        row.update(make_row(index, timestamp))
        rows.append(row)

    return rows


def write_csv(filename: str, rows):
    """
    Write generated data into a CSV file.
    """

    filepath = OUTPUT_DIR / filename

    if not rows:
        raise ValueError("No rows to write.")

    with open(filepath, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    return filepath