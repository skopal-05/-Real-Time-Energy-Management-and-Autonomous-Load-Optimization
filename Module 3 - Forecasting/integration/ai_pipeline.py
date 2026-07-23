from __future__ import annotations

import json

from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from production.production_forecast import ProductionForecast
from production.load_forecast import LoadForecast
from production.future_state_generator import FutureStateGenerator
from production.scenario_generator import ScenarioGenerator

from renewable.renewable_predictor import RenewablePredictor

from infrastructure.hvac_forecast import HVACForecast
from infrastructure.compressor_forecast import CompressorForecast
from infrastructure.boiler_forecast import BoilerForecast
from infrastructure.maintenance_predictor import MaintenancePredictor


class AIPipeline:

    def __init__(self):

        self.production = ProductionForecast()
        self.load = LoadForecast()

        self.renewable = RenewablePredictor()

        self.hvac = HVACForecast()
        self.compressor = CompressorForecast()
        self.boiler = BoilerForecast()

        self.maintenance = MaintenancePredictor()

        self.future_state = FutureStateGenerator()
        self.scenario = ScenarioGenerator()

        self.output_directory = Path("outputs/predictions")
        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    # --------------------------------------------------

    def run(
        self,
        sensor_data: Dict[str, Dict[str, Any]],
    ) -> Dict[str, Any]:

        # ---------------- Production ----------------

        production_prediction = self.production.forecast(
            sensor_data.get("production", {})
        )

        load_prediction = self.load.forecast(
            sensor_data.get("production", {})
        )

        # ---------------- Renewable ----------------

        renewable_prediction = self.renewable.predict(
            sensor_data.get("solar", {}),
            sensor_data.get("battery", {}),
            sensor_data.get("weather", {}),
        )

        # ---------------- Infrastructure ----------------

        hvac_prediction = self.hvac.forecast(
            sensor_data.get("hvac", {})
        )

        compressor_prediction = self.compressor.forecast(
            sensor_data.get("compressor", {})
        )

        boiler_prediction = self.boiler.forecast(
            sensor_data.get("boiler", {})
        )

        infrastructure = {

            "hvac": {
                "forecast": hvac_prediction,
                "maintenance": self.maintenance.predict(
                    "HVAC",
                    hvac_prediction,
                ),
            },

            "compressor": {
                "forecast": compressor_prediction,
                "maintenance": self.maintenance.predict(
                    "Compressor",
                    compressor_prediction,
                ),
            },

            "boiler": {
                "forecast": boiler_prediction,
                "maintenance": self.maintenance.predict(
                    "Boiler",
                    boiler_prediction,
                ),
            },
        }

        future_state = self.future_state.generate(
            production_prediction,
            load_prediction,
            renewable_prediction,
            infrastructure,
        )

        scenarios = self.scenario.generate(
            production_prediction,
            load_prediction,
        )

        return {

            "production": {
                "forecast": production_prediction,
                "load": load_prediction,
            },

            "renewable": renewable_prediction,

            "infrastructure": infrastructure,

            "future_state": future_state,

            "scenarios": scenarios,
        }

    # --------------------------------------------------

    def save_results(
        self,
        results: Dict[str, Any],
        filename: str = "forecast_results.json",
    ):

        output_root = Path("outputs")

        predictions_dir = output_root / "predictions"
        future_states_dir = output_root / "future_states"
        reports_dir = output_root / "reports"
        logs_dir = output_root / "logs"

        predictions_dir.mkdir(parents=True, exist_ok=True)
        future_states_dir.mkdir(parents=True, exist_ok=True)
        reports_dir.mkdir(parents=True, exist_ok=True)
        logs_dir.mkdir(parents=True, exist_ok=True)

        with open(predictions_dir / filename, "w", encoding="utf-8") as file:
            json.dump(results, file, indent=4)

        with open(future_states_dir / "future_state.json", "w", encoding="utf-8") as file:
            json.dump(results["future_state"], file, indent=4)

        report = {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "system_status": results["future_state"]["system_status"],
            "renewable_score": results["renewable"]["renewable_score"],
            "hvac_status": results["infrastructure"]["hvac"]["maintenance"]["status"],
            "compressor_status": results["infrastructure"]["compressor"]["maintenance"]["status"],
            "boiler_status": results["infrastructure"]["boiler"]["maintenance"]["status"],
            "available_scenarios": list(results["scenarios"].keys()),
        }

        with open(reports_dir / "forecast_report.json", "w", encoding="utf-8") as file:
            json.dump(report, file, indent=4)

        with open(logs_dir / "pipeline.log", "a", encoding="utf-8") as file:
            file.write(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                "Forecast pipeline executed successfully.\n"
            )