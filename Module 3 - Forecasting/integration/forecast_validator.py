from __future__ import annotations

from typing import Any, Dict


class ForecastValidator:

    def __init__(self):

        self.required_fields = {
            "hvac": [
                "predicted_temperature",
                "predicted_humidity",
                "predicted_power",
                "predicted_efficiency",
            ],
            "compressor": [
                "predicted_pressure",
                "predicted_airflow",
                "predicted_power",
                "health_score",
            ],
            "boiler": [
                "predicted_temperature",
                "predicted_pressure",
                "predicted_steam_flow",
                "predicted_fuel_consumption",
                "predicted_efficiency",
            ],
        }

    # ---------------------------------------------------------

    def validate(
        self,
        equipment: str,
        prediction: Dict[str, Any],
    ) -> bool:

        if equipment not in self.required_fields:
            return False

        for field in self.required_fields[equipment]:

            if field not in prediction:
                return False

            value = prediction[field]

            if value is None:
                return False

            if isinstance(value, (int, float)):

                if value < 0:
                    return False

        return True

    # ---------------------------------------------------------

    def validate_pipeline(
        self,
        results: Dict[str, Any],
    ) -> Dict[str, bool]:

        validation = {}

        for equipment in self.required_fields:

            forecast = results.get(
                equipment,
                {},
            ).get(
                "forecast",
                {},
            )

            validation[equipment] = self.validate(
                equipment,
                forecast,
            )

        validation["pipeline_valid"] = all(
            validation.values()
        )

        return validation