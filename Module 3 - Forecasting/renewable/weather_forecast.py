from __future__ import annotations

from typing import Any, Dict

from common.feature_builder import FeatureBuilder
from common.forecasting_base import ForecastingBase
from common.utils import current_timestamp, round_values


class WeatherForecast(ForecastingBase):

    def __init__(self, prediction_horizon: int = 60):

        super().__init__(
            model_name="Weather Forecast",
            prediction_horizon=prediction_horizon,
        )

        self.feature_builder = FeatureBuilder()

    def preprocess(self, sensor_data: Dict[str, Any]) -> Dict[str, Any]:

        return self.feature_builder.build(sensor_data)

    def predict(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:

        temperature = processed_data.get(
            "temperature",
            processed_data.get("temperature_avg", 30),
        )

        humidity = processed_data.get(
            "humidity",
            processed_data.get("humidity_avg", 60),
        )

        cloud_cover = processed_data.get(
            "cloud_cover",
            processed_data.get("cloud_cover_avg", 20),
        )

        return {
            "predicted_temperature": temperature + 0.2,
            "predicted_humidity": humidity - 0.5,
            "predicted_cloud_cover": cloud_cover + 1,
        }

    def postprocess(self, prediction: Dict[str, Any]) -> Dict[str, Any]:

        result = round_values(prediction)
        result["prediction_horizon"] = self.prediction_horizon
        result["timestamp"] = current_timestamp()

        return result