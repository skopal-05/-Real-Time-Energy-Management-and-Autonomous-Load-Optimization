from __future__ import annotations

from typing import Any, Dict

from common.feature_builder import FeatureBuilder
from common.forecasting_base import ForecastingBase
from common.utils import current_timestamp, round_values


class BatteryForecast(ForecastingBase):

    def __init__(self, prediction_horizon: int = 60):

        super().__init__(
            model_name="Battery Forecast",
            prediction_horizon=prediction_horizon,
        )

        self.feature_builder = FeatureBuilder()

    def preprocess(self, sensor_data: Dict[str, Any]) -> Dict[str, Any]:

        return self.feature_builder.build(sensor_data)

    def predict(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:

        soc = processed_data.get(
            "battery_soc",
            processed_data.get("battery_soc_avg", 80),
        )

        charge_rate = processed_data.get(
            "charge_rate",
            processed_data.get("charge_rate_avg", 5),
        )

        predicted_soc = min(
            soc + charge_rate,
            100,
        )

        return {
            "predicted_soc": predicted_soc,
            "predicted_charge_rate": charge_rate,
        }

    def postprocess(self, prediction: Dict[str, Any]) -> Dict[str, Any]:

        result = round_values(prediction)
        result["prediction_horizon"] = self.prediction_horizon
        result["timestamp"] = current_timestamp()

        return result