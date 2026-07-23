from __future__ import annotations

from typing import Any, Dict

from common.feature_builder import FeatureBuilder
from common.forecasting_base import ForecastingBase
from common.utils import current_timestamp, round_values


class BoilerForecast(ForecastingBase):
    """
    Forecast future boiler operating conditions.
    """

    def __init__(self, prediction_horizon: int = 60):

        super().__init__(
            model_name="Boiler Forecast",
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

        temperature = processed_data.get(
            "temperature",
            processed_data.get("temperature_avg", 150),
        )

        pressure = processed_data.get(
            "pressure",
            processed_data.get("pressure_avg", 8),
        )

        steam_flow = processed_data.get(
            "steam_flow",
            processed_data.get("steam_flow_avg", 100),
        )

        fuel_consumption = processed_data.get(
            "fuel_consumption",
            processed_data.get("fuel_consumption_avg", 50),
        )

        predicted_temperature = temperature + 0.30
        predicted_pressure = pressure + 0.15
        predicted_steam_flow = steam_flow + 2.0
        predicted_fuel_consumption = fuel_consumption * 1.02

        efficiency = max(
            0,
            100 - (predicted_fuel_consumption / 5),
        )

        return {
            "predicted_temperature": predicted_temperature,
            "predicted_pressure": predicted_pressure,
            "predicted_steam_flow": predicted_steam_flow,
            "predicted_fuel_consumption": predicted_fuel_consumption,
            "predicted_efficiency": efficiency,
        }

    def postprocess(
        self,
        prediction: Dict[str, Any],
    ) -> Dict[str, Any]:

        result = round_values(prediction)

        result["prediction_horizon"] = self.prediction_horizon
        result["timestamp"] = current_timestamp()

        return result