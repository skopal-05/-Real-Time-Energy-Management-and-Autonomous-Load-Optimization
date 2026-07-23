"""
Utility functions for AI Forecasting Module.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


# ---------------------------------------------------------
# Timestamp
# ---------------------------------------------------------

def current_timestamp() -> str:
    """
    Returns current timestamp.
    """

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ---------------------------------------------------------
# Create Directory
# ---------------------------------------------------------

def ensure_directory(path: str) -> Path:
    """
    Creates directory if it doesn't exist.
    """

    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)

    return directory


# ---------------------------------------------------------
# Save JSON
# ---------------------------------------------------------

def save_json(data: Dict[str, Any], filepath: str) -> None:
    """
    Save dictionary to JSON file.
    """

    filepath = Path(filepath)

    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4
        )


# ---------------------------------------------------------
# Load JSON
# ---------------------------------------------------------

def load_json(filepath: str) -> Dict[str, Any]:
    """
    Load JSON file.
    """

    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)


# ---------------------------------------------------------
# Clamp Value
# ---------------------------------------------------------

def clamp(value: float, minimum: float, maximum: float) -> float:
    """
    Restrict value between min and max.
    """

    return max(minimum, min(value, maximum))


# ---------------------------------------------------------
# Percentage Change
# ---------------------------------------------------------

def percentage_change(old: float, new: float) -> float:
    """
    Calculate percentage change.
    """

    if old == 0:
        return 0.0

    return ((new - old) / old) * 100


# ---------------------------------------------------------
# Round Dictionary Values
# ---------------------------------------------------------

def round_values(data: Dict[str, Any], digits: int = 2) -> Dict[str, Any]:

    rounded = {}

    for key, value in data.items():

        if isinstance(value, float):
            rounded[key] = round(value, digits)

        else:
            rounded[key] = value

    return rounded


# ---------------------------------------------------------
# Normalize Value
# ---------------------------------------------------------

def normalize(
    value: float,
    minimum: float,
    maximum: float
) -> float:
    """
    Normalize between 0 and 1.
    """

    if maximum == minimum:
        return 0.0

    return (value - minimum) / (maximum - minimum)


# ---------------------------------------------------------
# Future Timestamp
# ---------------------------------------------------------

def future_timestamp(minutes: int) -> str:
    """
    Returns future timestamp.
    """

    future = datetime.now().timestamp() + (minutes * 60)

    return datetime.fromtimestamp(
        future
    ).strftime("%Y-%m-%d %H:%M:%S")