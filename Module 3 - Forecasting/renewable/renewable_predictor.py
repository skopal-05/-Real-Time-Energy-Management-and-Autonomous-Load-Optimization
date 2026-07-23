from __future__ import annotations

from typing import Any, Dict

from renewable.solar_forecast import SolarForecast
from renewable.battery_forecast import BatteryForecast
from renewable.weather_forecast import WeatherForecast


class RenewablePredictor:

    def __init__(self):

        self.solar = SolarForecast()
        self.battery = BatteryForecast()
        self.weather = WeatherForecast()

    def predict(
        self,
        solar_data: Dict[str, Any],
        battery_data: Dict[str, Any],
        weather_data: Dict[str, Any],
    ) -> Dict[str, Any]:

        solar = self.solar.forecast(solar_data)

        battery = self.battery.forecast(battery_data)

        weather = self.weather.forecast(weather_data)

        renewable_score = (
            solar["predicted_solar_output"] * 0.5
            + battery["predicted_soc"] * 0.3
            + (100 - weather["predicted_cloud_cover"]) * 0.2
        )

        return {
            "solar": solar,
            "battery": battery,
            "weather": weather,
            "renewable_score": round(
                renewable_score,
                2,
            ),
        }