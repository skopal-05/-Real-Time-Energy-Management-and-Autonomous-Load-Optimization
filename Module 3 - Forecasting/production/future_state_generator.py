from __future__ import annotations

from typing import Any, Dict

from common.utils import current_timestamp


class FutureStateGenerator:

    def __init__(self):

        self.version = "1.0"

    # ---------------------------------------------------------

    def generate(
        self,
        production_forecast: Dict[str, Any],
        load_forecast: Dict[str, Any],
        renewable_forecast: Dict[str, Any] | None = None,
        infrastructure_forecast: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:

        future_state = {

            "timestamp": current_timestamp(),

            "version": self.version,

            "production": production_forecast,

            "load": load_forecast,

            "renewable": renewable_forecast or {},

            "infrastructure": infrastructure_forecast or {},

            "system_status": self._system_status(
                production_forecast,
                infrastructure_forecast,
            ),
        }

        return future_state

    # ---------------------------------------------------------

    def _system_status(
        self,
        production: Dict[str, Any],
        infrastructure: Dict[str, Any] | None,
    ) -> str:

        productivity = production.get(
            "productivity_score",
            100,
        )

        if productivity < 60:
            return "Critical"

        if productivity < 80:
            return "Warning"

        if infrastructure:

            for equipment in infrastructure.values():

                maintenance = equipment.get(
                    "maintenance",
                    {},
                )

                if maintenance.get("status") == "Critical":
                    return "Critical"

                if maintenance.get("status") == "Warning":
                    return "Warning"

        return "Healthy"