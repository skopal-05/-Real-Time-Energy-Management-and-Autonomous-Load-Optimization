import csv
import unittest
from pathlib import Path

from module2_digital_twin.boiler import BoilerDigitalTwin
from module2_digital_twin.production_line_a import ProductionLineADigitalTwin
from module2_digital_twin.production_line_b import ProductionLineBDigitalTwin


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "Module 1 - Data Acquisition" / "outputs"


class Person1DigitalTwinTests(unittest.TestCase):
    def _exercise(self, twin, filename):
        updates = twin.realtime_sync.sync_csv(DATA / filename)
        self.assertGreater(len(updates), 0)
        self.assertEqual(len(updates), len(twin.state_manager.history))
        result = twin.simulation.run()
        self.assertIn("predicted_metrics", result)
        self.assertGreater(twin.behavior_learner.samples_seen, 0)

    def test_production_line_a(self):
        self._exercise(ProductionLineADigitalTwin(), "production_line_a_production.csv")

    def test_production_line_b(self):
        self._exercise(ProductionLineBDigitalTwin(), "production_line_b_production.csv")

    def test_boiler(self):
        self._exercise(BoilerDigitalTwin(), "boiler.csv")

    def test_invalid_production_state_is_rejected(self):
        with (DATA / "production_line_a_production.csv").open(newline="", encoding="utf-8") as stream:
            state = next(csv.DictReader(stream))
        state["motor_temperature_c"] = "999"
        with self.assertRaises(ValueError):
            ProductionLineADigitalTwin().update(state)


if __name__ == "__main__":
    unittest.main()

