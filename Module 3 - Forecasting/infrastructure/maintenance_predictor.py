from __future__ import annotations

from typing import Dict, Any


class MaintenancePredictor:
    """
    Predicts equipment health based on forecast results.
    """

    def __init__(self):

        self.thresholds = {
            "temperature": 90,
            "pressure": 10,
            "power": 500,
            "efficiency": 70,
            "health_score": 70,
        }

    # ---------------------------------------------------------

    def predict(
        self,
        equipment: str,
        forecast: Dict[str, Any],
    ) -> Dict[str, Any]:

        issues = []

        # Temperature

        if (
            forecast.get("predicted_temperature", 0)
            > self.thresholds["temperature"]
        ):
            issues.append("High Temperature")

        # Pressure

        if (
            forecast.get("predicted_pressure", 0)
            > self.thresholds["pressure"]
        ):
            issues.append("High Pressure")

        # Power

        if (
            forecast.get("predicted_power", 0)
            > self.thresholds["power"]
        ):
            issues.append("High Power Consumption")

        # Efficiency

        if (
            forecast.get("predicted_efficiency", 100)
            < self.thresholds["efficiency"]
        ):
            issues.append("Low Efficiency")

        # Compressor Health

        if (
            forecast.get("health_score", 100)
            < self.thresholds["health_score"]
        ):
            issues.append("Low Health Score")

        # Overall Status

        if len(issues) == 0:
            status = "Healthy"

        elif len(issues) <= 2:
            status = "Warning"

        else:
            status = "Critical"

        return {
            "equipment": equipment,
            "status": status,
            "issues": issues,
            "maintenance_required": status != "Healthy",
        }

    # ---------------------------------------------------------

    def update_threshold(
        self,
        parameter: str,
        value: float,
    ) -> None:

        self.thresholds[parameter] = value

    # ---------------------------------------------------------

    def get_thresholds(self):

        return self.thresholds