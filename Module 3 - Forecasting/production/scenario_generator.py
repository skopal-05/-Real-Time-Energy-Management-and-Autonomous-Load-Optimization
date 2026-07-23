from __future__ import annotations

from typing import Any, Dict


class ScenarioGenerator:

    def __init__(self):

        self.scenarios = (
            "optimistic",
            "normal",
            "worst_case",
        )

    # ---------------------------------------------------------

    def generate(
        self,
        production_forecast: Dict[str, Any],
        load_forecast: Dict[str, Any],
    ) -> Dict[str, Dict[str, Any]]:

        return {

            "optimistic": self._optimistic(
                production_forecast,
                load_forecast,
            ),

            "normal": self._normal(
                production_forecast,
                load_forecast,
            ),

            "worst_case": self._worst_case(
                production_forecast,
                load_forecast,
            ),
        }

    # ---------------------------------------------------------

    def _optimistic(
        self,
        production: Dict[str, Any],
        load: Dict[str, Any],
    ) -> Dict[str, Any]:

        return {

            "production": round(
                production.get(
                    "predicted_production",
                    0,
                ) * 1.05,
                2,
            ),

            "energy_consumption": round(
                production.get(
                    "predicted_energy_consumption",
                    0,
                ) * 0.95,
                2,
            ),

            "load": round(
                load.get(
                    "predicted_load",
                    0,
                ) * 0.95,
                2,
            ),

            "status": "Healthy",
        }

    # ---------------------------------------------------------

    def _normal(
        self,
        production: Dict[str, Any],
        load: Dict[str, Any],
    ) -> Dict[str, Any]:

        return {

            "production": production.get(
                "predicted_production",
                0,
            ),

            "energy_consumption": production.get(
                "predicted_energy_consumption",
                0,
            ),

            "load": load.get(
                "predicted_load",
                0,
            ),

            "status": "Normal",
        }

    # ---------------------------------------------------------

    def _worst_case(
        self,
        production: Dict[str, Any],
        load: Dict[str, Any],
    ) -> Dict[str, Any]:

        return {

            "production": round(
                production.get(
                    "predicted_production",
                    0,
                ) * 0.90,
                2,
            ),

            "energy_consumption": round(
                production.get(
                    "predicted_energy_consumption",
                    0,
                ) * 1.10,
                2,
            ),

            "load": round(
                load.get(
                    "predicted_load",
                    0,
                ) * 1.15,
                2,
            ),

            "status": "Critical",
        }

    # ---------------------------------------------------------

    def available_scenarios(self):

        return list(self.scenarios)