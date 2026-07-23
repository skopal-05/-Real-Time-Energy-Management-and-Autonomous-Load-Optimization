"""
Centralized model manager for AI forecasting modules.
"""

from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any, Dict


class ModelManager:
    """
    Handles loading, saving and accessing forecasting models.
    """

    def __init__(self, model_directory: str = "models") -> None:

        self.model_directory = Path(model_directory)
        self.model_directory.mkdir(parents=True, exist_ok=True)

        self.models: Dict[str, Any] = {}

    # ---------------------------------------------------------
    # Register Model
    # ---------------------------------------------------------

    def register_model(self, model_name: str, model: Any) -> None:

        self.models[model_name] = model

    # ---------------------------------------------------------
    # Get Model
    # ---------------------------------------------------------

    def get_model(self, model_name: str):

        return self.models.get(model_name)

    # ---------------------------------------------------------
    # Remove Model
    # ---------------------------------------------------------

    def remove_model(self, model_name: str):

        if model_name in self.models:
            del self.models[model_name]

    # ---------------------------------------------------------
    # Save Model
    # ---------------------------------------------------------

    def save_model(self, model_name: str) -> bool:

        if model_name not in self.models:
            return False

        filepath = self.model_directory / f"{model_name}.pkl"

        with open(filepath, "wb") as file:
            pickle.dump(self.models[model_name], file)

        return True

    # ---------------------------------------------------------
    # Load Model
    # ---------------------------------------------------------

    def load_model(self, model_name: str) -> bool:

        filepath = self.model_directory / f"{model_name}.pkl"

        if not filepath.exists():
            return False

        with open(filepath, "rb") as file:
            self.models[model_name] = pickle.load(file)

        return True

    # ---------------------------------------------------------
    # Save All Models
    # ---------------------------------------------------------

    def save_all(self):

        for model_name in self.models:
            self.save_model(model_name)

    # ---------------------------------------------------------
    # Load All Models
    # ---------------------------------------------------------

    def load_all(self):

        for file in self.model_directory.glob("*.pkl"):

            with open(file, "rb") as f:
                self.models[file.stem] = pickle.load(f)

    # ---------------------------------------------------------
    # List Models
    # ---------------------------------------------------------

    def list_models(self):

        return list(self.models.keys())

    # ---------------------------------------------------------
    # Clear Models
    # ---------------------------------------------------------

    def clear(self):

        self.models.clear()

    # ---------------------------------------------------------
    # Model Information
    # ---------------------------------------------------------

    def info(self):

        return {
            "registered_models": len(self.models),
            "models": self.list_models(),
            "directory": str(self.model_directory),
        }

    def __len__(self):

        return len(self.models)

    def __contains__(self, model_name):

        return model_name in self.models

    def __str__(self):

        return (
            f"ModelManager("
            f"{len(self.models)} models)"
        )