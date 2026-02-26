import yaml
import pathlib
from typing import Dict, Any

class Config:
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = pathlib.Path(config_path)
        self.data: Dict[str, Any] = {}

    def load(self):
        """
        Loads the configuration from the YAML file.
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, "r") as f:
            self.data = yaml.safe_load(f)
        return self.data
