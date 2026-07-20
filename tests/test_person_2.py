import unittest
from pathlib import Path

from module2_digital_twin.battery import BatteryDigitalTwin
from module2_digital_twin.grid import GridDigitalTwin
from module2_digital_twin.solar import SolarDigitalTwin


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "Module 1 - Data Acquisition" / "outputs"


class Person2DigitalTwinTests(unittest.TestCase):
    def _exercise(self, twin, filename):
        updates = twin.realtime_sync.sync_csv(DATA / filename)
        self.assertGreater(len(updates), 0)
        result = twin.simulation.run()
        self.assertIn("predicted_metrics", result)
        self.assertGreater(twin.behavior_learner.samples_seen, 0)

    def test_solar(self):
        self._exercise(SolarDigitalTwin(), "solar_plant.csv")

    def test_battery(self):
        twin = BatteryDigitalTwin()
        self._exercise(twin, "battery_storage.csv")
        result = twin.simulation.run({"battery_power_kw": 50.0, "duration_hours": 1.0})
        self.assertEqual(result["predicted_metrics"]["power_mode"], "charging")

    def test_grid(self):
        twin = GridDigitalTwin()
        self._exercise(twin, "grid.csv")
        self.assertIsInstance(twin.simulation.run()["predicted_metrics"]["grid_stable"], bool)


if __name__ == "__main__":
    unittest.main()

