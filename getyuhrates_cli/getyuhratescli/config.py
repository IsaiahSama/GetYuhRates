"""Configuration management for GetYuhRates CLI.

This module handles loading and validating configuration from config.yaml
and environment variables from .env files.
"""

import os
from pathlib import Path
from typing import NotRequired, TypedDict

import yaml
from dotenv import load_dotenv


class RateLimitConfig(TypedDict):
    """Rate limiting configuration.

    Attributes:
        enabled: Whether rate limiting is enabled.
        delay_seconds: Delay between API requests in seconds.
        respect_headers: Whether to adjust delays based on API response headers.
    """
    enabled: bool
    delay_seconds: float
    respect_headers: bool


class Config(TypedDict):
    """Configuration structure for GetYuhRates CLI.

    Attributes:
        source: List of source currencies.
        currencies: List of target currencies.
        always_download: Whether to always download rates.
        output_folder: Path to folder for storing generated reports.
        output_format: Output format (CSV or PDF).
        send_emails: Whether to send emails with reports.
        sender_email: Email address of sender.
        recipients: List of recipient email addresses.
        subject_title: Email subject line.
        email_body: Email body text.
        rate_limit: Rate limiting configuration (optional).
    """
    source: list[str]
    currencies: list[str]
    always_download: str
    output_folder: str
    output_format: str
    send_emails: bool
    sender_email: str
    recipients: list[str]
    subject_title: str
    email_body: str
    rate_limit: NotRequired[RateLimitConfig]


class ConfigLoadError(Exception):
    """Exception raised when configuration cannot be loaded."""
    pass


class ConfigValidationError(Exception):
    """Exception raised when configuration is invalid."""
    pass


def load_env_file(env_path: Path | None = None) -> None:
    """Load environment variables from .env file.

    Args:
        env_path: Path to .env file. If None, searches for .env in current directory.

    Returns:
        None: Environment variables are loaded into os.environ.
    """
    if env_path is None:
        env_path = Path.cwd() / ".env"

    if env_path.exists():
        load_dotenv(dotenv_path=env_path)


def get_api_key() -> str:
    """Get CurrencyLayer API key from environment variables.

    Returns:
        str: The API key value.

    Raises:
        ConfigValidationError: If CURRENCYLAYER_API_KEY is not set.
    """
    api_key = os.getenv("CURRENCYLAYER_API_KEY")
    if not api_key:
        raise ConfigValidationError(
            "CURRENCYLAYER_API_KEY environment variable is not set. "
            "Please check your .env file."
        )
    return api_key


def get_rate_limit_config(config: Config) -> RateLimitConfig:
    """Get rate limiting configuration with sensible defaults.

    Args:
        config: Loaded configuration dictionary.

    Returns:
        RateLimitConfig: Rate limiting configuration with defaults applied.
    """
    default_config: RateLimitConfig = {
        "enabled": True,
        "delay_seconds": 1.0,
        "respect_headers": True,
    }

    if "rate_limit" not in config:
        return default_config

    rate_limit = config["rate_limit"]

    # Merge with defaults, allowing partial overrides
    return {
        "enabled": rate_limit.get("enabled", default_config["enabled"]),
        "delay_seconds": rate_limit.get("delay_seconds", default_config["delay_seconds"]),
        "respect_headers": rate_limit.get("respect_headers", default_config["respect_headers"]),
    }


def load_config(config_path: Path | None = None) -> Config:
    """Load configuration from config.yaml file.

    Args:
        config_path: Path to config.yaml file. If None, uses config.yaml in current directory.

    Returns:
        Config: Loaded and validated configuration.

    Raises:
        ConfigLoadError: If config file cannot be loaded.
        ConfigValidationError: If config file is missing required fields.
    """
    if config_path is None:
        config_path = Path.cwd() / "config.yaml"

    if not config_path.exists():
        raise ConfigLoadError(
            f"Configuration file not found: {config_path}\n"
            "Please create a config.yaml file based on config.yaml.example"
        )

    try:
        with open(config_path, "r") as f:
            config_data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ConfigLoadError(f"Invalid YAML in config file: {e}")
    except Exception as e:
        raise ConfigLoadError(f"Error reading config file: {e}")

    if not isinstance(config_data, dict):
        raise ConfigValidationError("Config file must contain a YAML object/dictionary")

    # Validate required fields
    required_fields = [
        "source",
        "currencies",
        "always_download",
        "output_folder",
        "output_format",
        "send_emails",
        "sender_email",
        "recipients",
        "subject_title",
        "email_body",
    ]

    missing_fields = [field for field in required_fields if field not in config_data]
    if missing_fields:
        raise ConfigValidationError(
            f"Missing required fields in config.yaml: {', '.join(missing_fields)}"
        )

    # Validate field types
    if not isinstance(config_data["source"], list):
        raise ConfigValidationError("'source' must be a list")
    if not isinstance(config_data["currencies"], list):
        raise ConfigValidationError("'currencies' must be a list")
    if not isinstance(config_data["recipients"], list):
        raise ConfigValidationError("'recipients' must be a list")

    return config_data  # type: ignore[return-value]


def validate_config(config_path: Path | None = None, env_path: Path | None = None) -> tuple[bool, str]:
    """Validate configuration file and environment variables.

    Args:
        config_path: Path to config.yaml file. If None, uses config.yaml in current directory.
        env_path: Path to .env file. If None, uses .env in current directory.

    Returns:
        tuple[bool, str]: A tuple of (success, message) indicating validation result.
    """
    messages: list[str] = []

    # Check config.yaml
    if config_path is None:
        config_path = Path.cwd() / "config.yaml"

    if not config_path.exists():
        return False, f"Configuration file not found: {config_path}"

    messages.append(f"Found config.yaml at: {config_path}")

    # Try to load and validate config
    try:
        config = load_config(config_path)
        messages.append("Config file is valid YAML")
        messages.append("All required fields are present")
        messages.append(f"  - Source currencies: {', '.join(config['source'])}")
        messages.append(f"  - Target currencies: {', '.join(config['currencies'])}")
        messages.append(f"  - Output folder: {config['output_folder']}")
        messages.append(f"  - Output format: {config['output_format']}")
    except ConfigLoadError as e:
        return False, f"Config load error:\n{str(e)}"
    except ConfigValidationError as e:
        return False, f"Config validation error:\n{str(e)}"

    # Check .env file
    if env_path is None:
        env_path = Path.cwd() / ".env"

    if not env_path.exists():
        messages.append(f"\nWarning: .env file not found at: {env_path}")
    else:
        messages.append(f"\nFound .env file at: {env_path}")
        load_env_file(env_path)

    # Check API key
    try:
        api_key = get_api_key()
        # Mask the API key for security
        masked_key = api_key[:4] + "..." + api_key[-4:] if len(api_key) > 8 else "***"
        messages.append(f"CURRENCYLAYER_API_KEY is set: {masked_key}")
    except ConfigValidationError as e:
        return False, "\n".join(messages) + f"\n\nError: {str(e)}"

    return True, "\n".join(messages)
