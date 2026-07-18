from __future__ import annotations

import csv
import math
import random
from datetime import datetime, timedelta
from pathlib import Path

# ==========================================================
# Project Paths
# ==========================================================

# data_collection/
CURRENT_DIR = Path(__file__).resolve().parent

# Module 1 - Data Acquisition/
PROJECT_DIR = CURRENT_DIR.parent

# Output folders
OUTPUT_DIR = PROJECT_DIR / "outputs"
CLEANED_DIR = OUTPUT_DIR / "cleaned_data"
LOG_DIR = OUTPUT_DIR / "logs"

# Create folders automatically
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CLEANED_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

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

def bounded(value: float, low: float, high: float) -> float:
    """
    Restrict a value between lower and upper limits.
    """
    return max(low, min(value, high))


def random_walk(
    start: float,
    periods: int,
    step: float = 1.0,
    low: float | None = None,
    high: float | None = None,
):
    """
    Generate a bounded random walk.

    Example:
    start = 8.2
    periods = 96
    """
    values = [round(start, 2)]

    for _ in range(periods - 1):
        next_value = values[-1] + random.uniform(-step, step)

        if low is not None:
            next_value = max(low, next_value)

        if high is not None:
            next_value = min(high, next_value)

        values.append(round(next_value, 2))

    return values