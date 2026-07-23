from __future__ import annotations

from typing import Any, Dict

from common.feature_builder import FeatureBuilder
from common.forecasting_base import ForecastingBase
from common.utils import current_timestamp, round_values


class LoadForecast(ForecastingBase):

    def __init__(self, prediction_horizon: int = 60):

        super().__init__(
            model_name="Load Forecast",
            prediction_horizon=prediction_horizon,
        )

        self.feature_builder = FeatureBuilder()

    def preprocess(
        self,
        sensor_data: Dict[str, Any],
    ) -> Dict[str, Any]:

        return self.feature_builder.build(sensor_data)

    def predict(
        self,
        processed_data: Dict[str, Any],
    ) -> Dict[str, Any]:

        production_rate = processed_data.get(
            "production_rate",
            processed_data.get("production_rate_avg", 100),
        )

        energy_consumption = processed_data.get(
            "energy_consumption",
            processed_data.get("energy_consumption_avg", 250),
        )

        machine_utilization = processed_data.get(
            "machine_utilization",
            processed_data.get("machine_utilization_avg", 80),
        )

        current_load = processed_data.get(
            "current_load",
            processed_data.get("current_load_avg", 70),
        )

        predicted_load = (
            current_load * 0.50 +
            machine_utilization * 0.30 +
            (production_rate / 10) * 0.20
        )

        peak_load = predicted_load * 1.10

        load_factor = (
            predicted_load / peak_load
            if peak_load > 0
            else 0
        )

        predicted_energy = energy_consumption * 1.02

        return {
            "predicted_load": predicted_load,
            "predicted_peak_load": peak_load,
            "load_factor": load_factor,
            "predicted_energy_consumption": predicted_energy,
        }

    def postprocess(
        self,
        prediction: Dict[str, Any],
    ) -> Dict[str, Any]:

        result = round_values(prediction)

        result["prediction_horizon"] = self.prediction_horizon
        result["timestamp"] = current_timestamp()

        return result