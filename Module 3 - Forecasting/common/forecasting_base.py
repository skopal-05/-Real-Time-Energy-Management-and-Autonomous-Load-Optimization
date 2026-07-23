"""
Base class for all forecasting modules used in the
Generative Digital Twin AI Forecasting System.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any


class ForecastingBase(ABC):
    """
    Abstract base class for all forecasting models.

    Every forecasting module (HVAC, Boiler, Compressor,
    Solar, Battery, Production etc.) should inherit from
    this class.
    """

    def __init__(
        self,
        model_name: str,
        prediction_horizon: int = 60,
    ) -> None:
        """
        Parameters
        ----------
        model_name : str
            Name of forecasting model.

        prediction_horizon : int
            Future prediction window (minutes).
        """

        self.model_name = model_name
        self.prediction_horizon = prediction_horizon
        self.last_prediction = None
        self.last_timestamp = None

    @abstractmethod
    def preprocess(self, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare sensor data before prediction.
        """
        pass

    @abstractmethod
    def predict(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate future prediction.
        """
        pass

    @abstractmethod
    def postprocess(self, prediction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply post-processing to prediction.
        """
        pass

    def forecast(self, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Complete forecasting pipeline.

        Sensor Data
              ↓
        Preprocess
              ↓
        Predict
              ↓
        Postprocess
        """

        processed = self.preprocess(sensor_data)

        prediction = self.predict(processed)

        result = self.postprocess(prediction)

        self.last_prediction = result
        self.last_timestamp = datetime.now()

        return result

    def get_last_prediction(self):

        return self.last_prediction

    def get_last_timestamp(self):

        return self.last_timestamp

    def reset(self):

        self.last_prediction = None
        self.last_timestamp = None

    def info(self) -> Dict[str, Any]:

        return {
            "model_name": self.model_name,
            "prediction_horizon": self.prediction_horizon,
            "last_prediction": self.last_prediction,
            "last_timestamp": self.last_timestamp,
        }

    def __str__(self):

        return (
            f"{self.model_name}"
            f"(Horizon={self.prediction_horizon} min)"
        )