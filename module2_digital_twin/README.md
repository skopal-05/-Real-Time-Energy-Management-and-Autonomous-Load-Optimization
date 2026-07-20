# Module 2 - Generative Industrial Digital Twin

This Week 2 module implements all work assigned to Person 1 and Person 2. It consumes telemetry produced by the repository's `Module 1 - Data Acquisition` and provides state validation, online behaviour learning, CSV-based live synchronization, and non-destructive scenario simulation.

## Responsibility map

- Person 1: `production_line_a/`, `production_line_b/`, and `boiler/`
- Person 2: `solar/`, `battery/`, and `grid/`
- Person 3 work (`hvac/`, `compressor/`, `common/`, and system integration) is intentionally outside this delivery.

Each system contains the five files required by the Week 2 brief:

- `digital_twin.py`
- `state_manager.py`
- `behavior_learning.py`
- `realtime_sync.py`
- `simulation.py`

The assigned research topics and implementation rationale are documented in `RESEARCH.md`. Step-by-step verification is documented in `MANUAL_CHECKS.md`.

## Run the tests

From the repository root:

```bash
python3 -m unittest discover -s module2_digital_twin/tests -v
```

In the local workspace, where the module is wrapped in a `Module 2` directory, use:

```bash
PYTHONPATH="Module 2" python3 -m unittest discover \
  -s "Module 2/module2_digital_twin/tests" -v
```

The tests synchronize all six twins against their corresponding Week 1 CSV files and verify validation, behaviour updates, duplicate filtering, and simulations.

## Example

```bash
python3 - <<'PY'
from module2_digital_twin.solar import SolarDigitalTwin

twin = SolarDigitalTwin()
twin.realtime_sync.sync_csv(
    "Module 1 - Data Acquisition/outputs/solar_plant.csv"
)
result = twin.simulation.run({"irradiance_w_m2": 900})
print(result["predicted_metrics"])
PY
```

`sync_csv(path, only_new=True)` filters already processed timestamps. `simulation.run(overrides)` creates a what-if result without modifying the live state. Use `simulation.save(result, path)` to save a JSON result under `outputs/simulation_results/`.
