from __future__ import annotations

from typing import Any, Dict

from common.feature_builder import FeatureBuilder
from common.forecasting_base import ForecastingBase
from common.utils import current_timestamp, round_values


class CompressorForecast(ForecastingBase):
    """
    Forecast future compressor operating conditions.
    """

    def __init__(self, prediction_horizon: int = 60):

        super().__init__(
            model_name="Compressor Forecast",
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

        pressure = processed_data.get(
            "pressure",
            processed_data.get("pressure_avg", 7.0),
        )

        airflow = processed_data.get(
            "airflow",
            processed_data.get("airflow_avg", 120),
        )

        power = processed_data.get(
            "power",
            processed_data.get("power_avg", 0),
        )

        predicted_pressure = pressure + 0.10
        predicted_airflow = airflow - 1.5
        predicted_power = power * 1.02

        health_score = max(
            0,
            100 - (predicted_power / 25),
        )

        return {
            "predicted_pressure": predicted_pressure,
            "predicted_airflow": predicted_airflow,
            "predicted_power": predicted_power,
            "health_score": health_score,
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