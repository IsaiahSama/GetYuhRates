"""Routes for configuration management."""

from typing import Any

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..models.requests import ConfigUpdateRequest
from ..models.responses import MessageResponse, ConfigResponse
from ..config import ConfigManager

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Common currency codes
AVAILABLE_CURRENCIES = [
    "USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY",
    "BBD", "PLN", "SEK", "NOK", "DKK", "NZD", "SGD", "HKD",
    "KRW", "MXN", "INR", "BRL", "ZAR", "RUB", "TRY"
]


@router.get("/config", response_class=HTMLResponse)
async def config_page(request: Request) -> Any:
    """Render the configuration management page.

    Args:
        request (Request): The HTTP request object.

    Returns:
        Any: Rendered HTML template.
    """
    config_manager = ConfigManager()

    try:
        config = config_manager.read_config()
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Configuration file not found. Please create config.yaml from config.yaml.example"
        )

    return templates.TemplateResponse(
        "config.html",
        {
            "request": request,
            "config": config,
            "available_currencies": AVAILABLE_CURRENCIES,
        }
    )


@router.get("/config/data", response_model=ConfigResponse)
async def get_config() -> dict[str, Any]:
    """Get current configuration as JSON.

    Returns:
        dict[str, Any]: Current configuration data.

    Raises:
        HTTPException: If configuration file cannot be read.
    """
    config_manager = ConfigManager()

    try:
        config = config_manager.read_config()
        return config
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Configuration file not found"
        )


@router.post("/config/update", response_model=MessageResponse)
async def update_config(config_request: ConfigUpdateRequest) -> dict[str, Any]:
    """Update configuration settings.

    Note: The output_folder setting is preserved and cannot be modified.

    Args:
        config_request (ConfigUpdateRequest): The configuration update request.

    Returns:
        dict[str, Any]: Success message.

    Raises:
        HTTPException: If configuration cannot be updated.
    """
    config_manager = ConfigManager()

    try:
        # Convert Pydantic model to dict
        new_config = {
            "source": config_request.source,
            "currencies": config_request.currencies,
            "always_download": config_request.always_download,
            "output_format": config_request.output_format,
            "send_emails": config_request.send_emails,
            "sender_email": config_request.sender_email,
            "recipients": config_request.recipients,
            "subject_title": config_request.subject_title,
            "email_body": config_request.email_body,
        }

        # Write configuration (output_folder will be preserved)
        config_manager.write_config(new_config)

        return {
            "message": "Configuration updated successfully",
            "success": True
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error updating configuration: {str(e)}"
        )
