"""
Evaluation metrics for AI forecasting models.
"""

from __future__ import annotations

from math import sqrt
from typing import List


class ForecastMetrics:
    """
    Provides common regression metrics for forecasting models.
    """

    @staticmethod
    def mae(actual: List[float], predicted: List[float]) -> float:
        """
        Mean Absolute Error
        """

        if len(actual) != len(predicted):
            raise ValueError("Length mismatch.")

        if len(actual) == 0:
            return 0.0

        error = sum(abs(a - p) for a, p in zip(actual, predicted))

        return error / len(actual)

    # ---------------------------------------------------------

    @staticmethod
    def mse(actual: List[float], predicted: List[float]) -> float:
        """
        Mean Squared Error
        """

        if len(actual) != len(predicted):
            raise ValueError("Length mismatch.")

        if len(actual) == 0:
            return 0.0

        error = sum((a - p) ** 2 for a, p in zip(actual, predicted))

        return error / len(actual)

    # ---------------------------------------------------------

    @staticmethod
    def rmse(actual: List[float], predicted: List[float]) -> float:
        """
        Root Mean Squared Error
        """

        return sqrt(
            ForecastMetrics.mse(actual, predicted)
        )

    # ---------------------------------------------------------

    @staticmethod
    def mape(actual: List[float], predicted: List[float]) -> float:
        """
        Mean Absolute Percentage Error
        """

        if len(actual) != len(predicted):
            raise ValueError("Length mismatch.")

        values = []

        for a, p in zip(actual, predicted):

            if a != 0:
                values.append(abs((a - p) / a))

        if not values:
            return 0.0

        return (sum(values) / len(values)) * 100

    # ---------------------------------------------------------

    @staticmethod
    def accuracy(actual: List[float], predicted: List[float]) -> float:
        """
        Forecast Accuracy (%)
        """

        return max(
            0.0,
            100 - ForecastMetrics.mape(actual, predicted)
        )

    # ---------------------------------------------------------

    @staticmethod
    def summary(actual: List[float], predicted: List[float]):

        return {
            "MAE": round(
                ForecastMetrics.mae(actual, predicted), 4
            ),
            "MSE": round(
                ForecastMetrics.mse(actual, predicted), 4
            ),
            "RMSE": round(
                ForecastMetrics.rmse(actual, predicted), 4
            ),
            "MAPE": round(
                ForecastMetrics.mape(actual, predicted), 2
            ),
            "Accuracy": round(
                ForecastMetrics.accuracy(actual, predicted), 2
            ),
        }