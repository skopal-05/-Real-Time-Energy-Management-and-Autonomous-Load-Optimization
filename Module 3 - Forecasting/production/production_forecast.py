from __future__ import annotations

from typing import Any, Dict

from common.feature_builder import FeatureBuilder
from common.forecasting_base import ForecastingBase
from common.utils import current_timestamp, round_values


class ProductionForecast(ForecastingBase):
    """
    Forecast future production performance.
    """

    def __init__(self, prediction_horizon: int = 60):

        super().__init__(
            model_name="Production Forecast",
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

        machine_utilization = processed_data.get(
            "machine_utilization",
            processed_data.get("machine_utilization_avg", 80),
        )

        energy_consumption = processed_data.get(
            "energy_consumption",
            processed_data.get("energy_consumption_avg", 250),
        )

        defect_rate = processed_data.get(
            "defect_rate",
            processed_data.get("defect_rate_avg", 2),
        )

        predicted_production = production_rate * 1.02
        predicted_utilization = min(
            machine_utilization + 1,
            100,
        )

        predicted_energy = energy_consumption * 1.01

        predicted_defects = max(
            defect_rate - 0.1,
            0,
        )

        productivity_score = max(
            0,
            min(
                100,
                predicted_utilization - predicted_defects,
            ),
        )

        return {
            "predicted_production": predicted_production,
            "predicted_utilization": predicted_utilization,
            "predicted_energy_consumption": predicted_energy,
            "predicted_defect_rate": predicted_defects,
            "productivity_score": productivity_score,
        }

    def postprocess(
        self,
        prediction: Dict[str, Any],
    ) -> Dict[str, Any]:

        result = round_values(prediction)

        result["prediction_horizon"] = self.prediction_horizon
        result["timestamp"] = current_timestamp()

        return result