"""Configuration management utilities for the GetYuhRates web application."""

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv


class ConfigManager:
    """Manages application configuration from config.yaml.

    This class handles reading and writing configuration values,
    excluding the output_folder which is read-only.

    Attributes:
        config_path (Path): Path to the configuration file.
    """

    def __init__(self, config_path: str | Path = "config.yaml") -> None:
        """Initialize the configuration manager.

        Args:
            config_path (str | Path): Path to the config.yaml file.
        """
        self.config_path = Path(config_path)

    def read_config(self) -> dict[str, Any]:
        """Read the configuration file.

        Returns:
            dict[str, Any]: Configuration data.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        if config is None:
            return {}

        return config

    def write_config(self, config: dict[str, Any]) -> None:
        """Write configuration to file.

        Note: This preserves the output_folder value from the existing config
        and does not allow it to be modified.

        Args:
            config (dict[str, Any]): Configuration data to write.

        Raises:
            FileNotFoundError: If config file doesn't exist.
        """
        # Read existing config to preserve output_folder
        existing_config = self.read_config()

        # Preserve output_folder if it exists
        if "output_folder" in existing_config:
            config["output_folder"] = existing_config["output_folder"]

        with open(self.config_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(config, f, default_flow_style=False, sort_keys=False)

    def get_value(self, key: str, default: Any = None) -> Any:
        """Get a specific configuration value.

        Args:
            key (str): Configuration key.
            default (Any): Default value if key not found.

        Returns:
            Any: Configuration value.
        """
        config = self.read_config()
        return config.get(key, default)

    def set_value(self, key: str, value: Any) -> None:
        """Set a specific configuration value.

        Note: Cannot set output_folder.

        Args:
            key (str): Configuration key.
            value (Any): Configuration value.

        Raises:
            ValueError: If trying to set output_folder.
        """
        if key == "output_folder":
            raise ValueError("Cannot modify output_folder setting")

        config = self.read_config()
        config[key] = value
        self.write_config(config)


def load_env() -> None:
    """Load environment variables from .env file."""
    load_dotenv()


def get_api_key() -> str | None:
    """Get the CurrencyLayer API key from environment.

    Returns:
        str | None: API key if set, None otherwise.
    """
    return os.getenv("CURRENCYLAYER_API_KEY")


def get_reports_dir() -> Path:
    """Get the reports directory path.

    Returns:
        Path: Path to the reports directory.
    """
    config_manager = ConfigManager()
    output_folder = config_manager.get_value("output_folder", "./reports/")
    reports_path = Path(output_folder)

    # Create directory if it doesn't exist
    reports_path.mkdir(parents=True, exist_ok=True)

    return reports_path
