import json
from integration.ai_pipeline import AIPipeline
from integration.forecast_validator import ForecastValidator


def main():

    pipeline = AIPipeline()

    validator = ForecastValidator()

    sensor_data = {

        "production": {
            "production_rate": 120,
            "machine_utilization": 82,
            "energy_consumption": 275,
            "current_load": 72,
            "defect_rate": 1.5,
        },

        "solar": {
            "solar_irradiance": 800,
            "panel_efficiency": 92,
        },

        "battery": {
            "battery_soc": 80,
            "charge_rate": 4,
        },

        "weather": {
            "temperature": 31,
            "humidity": 58,
            "cloud_cover": 15,
        },

        "hvac": {
            "temperature": 24,
            "humidity": 50,
            "power": 420,
        },

        "compressor": {
            "pressure": 7.2,
            "airflow": 125,
            "power": 315,
        },

        "boiler": {
            "temperature": 155,
            "pressure": 8.5,
            "steam_flow": 105,
            "fuel_consumption": 58,
        },
    }

    print("=" * 60)
    print("Running AI Forecasting Pipeline...")
    print("=" * 60)

    results = pipeline.run(sensor_data)

    pipeline.save_results(results)

    print("\n========== PRODUCTION ==========")

    for k, v in results["production"]["forecast"].items():
        print(f"{k}: {v}")

    print("\n---------- LOAD ----------")

    for k, v in results["production"]["load"].items():
        print(f"{k}: {v}")

    print("\n========== RENEWABLE ==========")

    print("\nSolar")

    for k, v in results["renewable"]["solar"].items():
        print(f"{k}: {v}")

    print("\nBattery")

    for k, v in results["renewable"]["battery"].items():
        print(f"{k}: {v}")

    print("\nWeather")

    for k, v in results["renewable"]["weather"].items():
        print(f"{k}: {v}")

    print("\nRenewable Score:",
          results["renewable"]["renewable_score"])

    print("\n========== INFRASTRUCTURE ==========")

    for equipment, value in results["infrastructure"].items():

        print(f"\n{equipment.upper()}")

        print("Forecast")

        for k, v in value["forecast"].items():
            print(f"  {k}: {v}")

        print("\nMaintenance")

        for k, v in value["maintenance"].items():
            print(f"  {k}: {v}")

    print("\n========== FUTURE STATE ==========\n")

    print(json.dumps(results["future_state"], indent=4))

    print("\n========== SCENARIOS ==========")

    for name, scenario in results["scenarios"].items():

        print(f"\n{name.upper()}")

        for k, v in scenario.items():
            print(f"  {k}: {v}")

    infrastructure_results = results["infrastructure"]

    validation = validator.validate_pipeline(infrastructure_results)

    print("\n========== VALIDATION ==========")

    for k, v in validation.items():
        print(f"{k}: {v}")

    if validation["pipeline_valid"]:
        print("\nIntegration Test Passed")
    else:
        print("\nIntegration Test Failed")


if __name__ == "__main__":
    main()