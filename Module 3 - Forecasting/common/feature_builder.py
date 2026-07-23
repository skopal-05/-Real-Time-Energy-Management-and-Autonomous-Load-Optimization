"""
Builds AI-ready features from Digital Twin sensor data.
"""

from __future__ import annotations

from statistics import mean
from typing import Dict, Any, List


class FeatureBuilder:
    """
    Converts raw sensor data into forecasting features.
    """

    def __init__(self):

        self.history: List[Dict[str, Any]] = []

    # ---------------------------------------------------------
    # Store Sensor History
    # ---------------------------------------------------------

    def update(self, sensor_data: Dict[str, Any]) -> None:

        self.history.append(sensor_data)

        if len(self.history) > 100:
            self.history.pop(0)

    # ---------------------------------------------------------
    # Build Features
    # ---------------------------------------------------------

    def build(self, sensor_data: Dict[str, Any]) -> Dict[str, float]:

        self.update(sensor_data)

        features = {}

        for key, value in sensor_data.items():

            if isinstance(value, (int, float)):
                features[key] = float(value)

        features["history_size"] = len(self.history)

        features.update(self._moving_averages())

        return features

    # ---------------------------------------------------------
    # Moving Average Features
    # ---------------------------------------------------------

    def _moving_averages(self) -> Dict[str, float]:

        result = {}

        if len(self.history) < 2:
            return result

        numeric_keys = []

        for key, value in self.history[-1].items():
            if isinstance(value, (int, float)):
                numeric_keys.append(key)

        for key in numeric_keys:

            values = []

            for sample in self.history:

                if key in sample:
                    values.append(sample[key])

            if values:
                result[f"{key}_avg"] = mean(values)

        return result

    # ---------------------------------------------------------
    # Reset
    # ---------------------------------------------------------

    def reset(self):

        self.history.clear()

    # ---------------------------------------------------------
    # Get History
    # ---------------------------------------------------------

    def get_history(self):

        return self.history

    # ---------------------------------------------------------
    # Information
    # ---------------------------------------------------------

    def info(self):

        return {
            "samples": len(self.history)
        }

    def __len__(self):

        return len(self.history)

    def __str__(self):

        return (
            f"FeatureBuilder("
            f"samples={len(self.history)})"
        )