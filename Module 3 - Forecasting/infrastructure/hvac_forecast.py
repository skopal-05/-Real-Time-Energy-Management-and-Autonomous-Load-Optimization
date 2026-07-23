from __future__ import annotations

from typing import Any, Dict

from common.feature_builder import FeatureBuilder
from common.forecasting_base import ForecastingBase
from common.utils import current_timestamp, round_values


class HVACForecast(ForecastingBase):
    """
    Forecast future HVAC operating conditions.
    """

    def __init__(self, prediction_horizon: int = 60):

        super().__init__(
            model_name="HVAC Forecast",
            prediction_horizon=prediction_horizon,
        )

        self.feature_builder = FeatureBuilder()

    # ---------------------------------------------------------

    def preprocess(
        self,
        sensor_data: Dict[str, Any],
    ) -> Dict[str, Any]:

        return self.feature_builder.build(sensor_data)

    # ---------------------------------------------------------

    def predict(
        self,
        processed_data: Dict[str, Any],
    ) -> Dict[str, Any]:

        temperature = processed_data.get(
            "temperature",
            processed_data.get("temperature_avg", 25),
        )

        humidity = processed_data.get(
            "humidity",
            processed_data.get("humidity_avg", 50),
        )

        power = processed_data.get(
            "power",
            processed_data.get("power_avg", 0),
        )

        predicted_temperature = temperature + 0.15

        predicted_humidity = humidity - 0.25

        predicted_power = power * 1.03

        efficiency = max(
            0,
            100 - (predicted_power / 20),
        )

        return {
            "predicted_temperature": predicted_temperature,
            "predicted_humidity": predicted_humidity,
            "predicted_power": predicted_power,
            "predicted_efficiency": efficiency,
        }

    # ---------------------------------------------------------

    def postprocess(
        self,
        prediction: Dict[str, Any],
    ) -> Dict[str, Any]:

        result = round_values(prediction)

        result["prediction_horizon"] = self.prediction_horizon

        result["timestamp"] = current_timestamp()

        return result