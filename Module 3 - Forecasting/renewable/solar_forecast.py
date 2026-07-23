from __future__ import annotations

from typing import Any, Dict

from common.feature_builder import FeatureBuilder
from common.forecasting_base import ForecastingBase
from common.utils import current_timestamp, round_values


class SolarForecast(ForecastingBase):

    def __init__(self, prediction_horizon: int = 60):

        super().__init__(
            model_name="Solar Forecast",
            prediction_horizon=prediction_horizon,
        )

        self.feature_builder = FeatureBuilder()

    def preprocess(self, sensor_data: Dict[str, Any]) -> Dict[str, Any]:

        return self.feature_builder.build(sensor_data)

    def predict(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:

        solar_irradiance = processed_data.get(
            "solar_irradiance",
            processed_data.get("solar_irradiance_avg", 700),
        )

        panel_efficiency = processed_data.get(
            "panel_efficiency",
            processed_data.get("panel_efficiency_avg", 90),
        )

        power_output = (
            solar_irradiance * panel_efficiency
        ) / 1000

        return {
            "predicted_solar_output": power_output,
            "predicted_efficiency": panel_efficiency,
        }

    def postprocess(self, prediction: Dict[str, Any]) -> Dict[str, Any]:

        result = round_values(prediction)
        result["prediction_horizon"] = self.prediction_horizon
        result["timestamp"] = current_timestamp()

        return result