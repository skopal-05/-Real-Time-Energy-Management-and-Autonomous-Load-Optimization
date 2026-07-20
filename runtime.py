"""Small dependency-free runtime used by the Week 2 digital twins."""

from __future__ import annotations

import csv
import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable


def _number(value: Any) -> Any:
    """Convert numeric CSV cells while leaving labels unchanged."""
    if not isinstance(value, str):
        return value
    value = value.strip()
    try:
        return float(value)
    except ValueError:
        return value


class StateManager:
    """Validate state updates and retain an auditable state history."""

    def __init__(self, required_fields: Iterable[str], ranges: dict[str, tuple[float, float]]):
        self.required_fields = tuple(required_fields)
        self.ranges = dict(ranges)
        self._state: dict[str, Any] = {}
        self._history: list[dict[str, Any]] = []

    def update(self, state: dict[str, Any]) -> dict[str, Any]:
        candidate = {key: _number(value) for key, value in state.items()}
        missing = [field for field in self.required_fields if field not in candidate]
        if missing:
            raise ValueError(f"Missing required state fields: {', '.join(missing)}")
        for field, (low, high) in self.ranges.items():
            if field not in candidate:
                continue
            value = candidate[field]
            if not isinstance(value, (int, float)) or not low <= float(value) <= high:
                raise ValueError(f"{field} must be between {low} and {high}; received {value!r}")
        candidate["synchronized_at"] = datetime.now(timezone.utc).isoformat()
        self._state = candidate
        self._history.append(deepcopy(candidate))
        return self.snapshot()

    def snapshot(self) -> dict[str, Any]:
        return deepcopy(self._state)

    @property
    def history(self) -> list[dict[str, Any]]:
        return deepcopy(self._history)


class BehaviorLearner:
    """Learn an online linear model from synchronized sensor observations."""

    def __init__(self, features: Iterable[str], target: str, learning_rate: float = 0.01):
        self.features = tuple(features)
        self.target = target
        self.learning_rate = learning_rate
        self.intercept = 0.0
        self.weights = {feature: 0.0 for feature in self.features}
        self.samples_seen = 0

    def predict(self, state: dict[str, Any]) -> float:
        return self.intercept + sum(
            self.weights[field] * float(state[field]) for field in self.features
        )

    def observe(self, state: dict[str, Any]) -> float | None:
        if self.target not in state or any(field not in state for field in self.features):
            return None
        target = float(state[self.target])
        prediction = self.predict(state)
        error = target - prediction
        scale = max(1.0, sum(abs(float(state[field])) for field in self.features))
        step = self.learning_rate / scale
        self.intercept += step * error
        for field in self.features:
            self.weights[field] += step * error * float(state[field]) / scale
        self.samples_seen += 1
        return error

    def fit(self, states: Iterable[dict[str, Any]], epochs: int = 8) -> "BehaviorLearner":
        rows = list(states)
        for _ in range(max(1, epochs)):
            for state in rows:
                self.observe(state)
        return self

    def parameters(self) -> dict[str, Any]:
        return {
            "target": self.target,
            "features": list(self.features),
            "intercept": self.intercept,
            "weights": dict(self.weights),
            "samples_seen": self.samples_seen,
        }


class RealtimeSynchronizer:
    """Synchronize a twin with rows arriving in a CSV telemetry source."""

    def __init__(self, update_callback: Callable[[dict[str, Any]], dict[str, Any]]):
        self.update_callback = update_callback
        self.last_source_timestamp: str | None = None

    def sync_state(self, state: dict[str, Any]) -> dict[str, Any]:
        timestamp = str(state.get("timestamp", ""))
        result = self.update_callback(state)
        self.last_source_timestamp = timestamp or self.last_source_timestamp
        return result

    def sync_csv(self, path: str | Path, only_new: bool = False) -> list[dict[str, Any]]:
        updates: list[dict[str, Any]] = []
        with Path(path).open(newline="", encoding="utf-8") as stream:
            for row in csv.DictReader(stream):
                if only_new and self.last_source_timestamp and row.get("timestamp", "") <= self.last_source_timestamp:
                    continue
                updates.append(self.sync_state(row))
        return updates


class Simulator:
    """Run deterministic scenarios without changing the twin's live state."""

    def __init__(self, snapshot: Callable[[], dict[str, Any]], model: Callable[[dict[str, Any]], dict[str, Any]]):
        self.snapshot = snapshot
        self.model = model

    def run(self, overrides: dict[str, Any] | None = None) -> dict[str, Any]:
        scenario = self.snapshot()
        if not scenario:
            raise RuntimeError("Synchronize the digital twin before running a simulation")
        scenario.update(overrides or {})
        return self.model(scenario)

    def save(self, result: dict[str, Any], path: str | Path) -> Path:
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(result, indent=2), encoding="utf-8")
        return destination


class DigitalTwinBase:
    """Compose state, learning, synchronization, and simulation services."""

    def __init__(
        self,
        name: str,
        required_fields: Iterable[str],
        ranges: dict[str, tuple[float, float]],
        features: Iterable[str],
        target: str,
    ):
        self.name = name
        self.state_manager = StateManager(required_fields, ranges)
        self.behavior_learner = BehaviorLearner(features, target)
        self.realtime_sync = RealtimeSynchronizer(self.update)
        self.simulation = Simulator(self.state_manager.snapshot, self._simulate)

    def update(self, state: dict[str, Any]) -> dict[str, Any]:
        snapshot = self.state_manager.update(state)
        self.behavior_learner.observe(snapshot)
        return snapshot

    def _simulate(self, state: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    def predict_target(self, scenario: dict[str, Any]) -> float:
        """Anchor learned scenario deltas to the latest measured target value."""
        live = self.state_manager.snapshot()
        target = self.behavior_learner.target
        baseline = float(live.get(target, scenario.get(target, 0.0)))
        if not live or not self.behavior_learner.samples_seen:
            return baseline
        learned_delta = self.behavior_learner.predict(scenario) - self.behavior_learner.predict(live)
        return baseline + learned_delta

    @staticmethod
    def _result(state: dict[str, Any], **metrics: Any) -> dict[str, Any]:
        return {"input_state": state, "predicted_metrics": metrics}
