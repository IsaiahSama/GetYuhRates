"""Routes for currency rate requests."""

from pathlib import Path
from typing import Any

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..models.requests import CurrencyRateRequest
from ..models.responses import CurrencyRateResponse
from ..config import ConfigManager, get_api_key

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Common currency codes
AVAILABLE_CURRENCIES = [
    "USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY",
    "BBD", "PLN", "SEK", "NOK", "DKK", "NZD", "SGD", "HKD",
    "KRW", "MXN", "INR", "BRL", "ZAR", "RUB", "TRY"
]


@router.get("/rates", response_class=HTMLResponse)
async def rates_page(request: Request) -> Any:
    """Render the currency rates request page.

    Args:
        request (Request): The HTTP request object.

    Returns:
        Any: Rendered HTML template.
    """
    config_manager = ConfigManager()
    config = config_manager.read_config()

    default_source = config.get("source", ["USD"])
    default_currencies = config.get("currencies", ["EUR"])

    return templates.TemplateResponse(
        "rates.html",
        {
            "request": request,
            "available_currencies": AVAILABLE_CURRENCIES,
            "default_source": default_source,
            "default_currencies": default_currencies,
        }
    )


@router.post("/rates/fetch", response_model=list[CurrencyRateResponse])
async def fetch_rates(rate_request: CurrencyRateRequest) -> list[dict[str, Any]]:
    """Fetch currency exchange rates from CurrencyLayer API.

    Args:
        rate_request (CurrencyRateRequest): The rate request parameters.

    Returns:
        list[dict[str, Any]]: List of currency rate results.

    Raises:
        HTTPException: If API key is not configured or other errors occur.
    """
    api_key = get_api_key()
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="CURRENCYLAYER_API_KEY not configured. Please set it in .env file."
        )

    try:
        # Import here to handle potential import issues gracefully
        # type: ignore - ignoring type errors from getyuhrates package as it's in development
        from getyuhrates import GetYuhRates  # type: ignore
        from getyuhrates.csv_writer import CSVWriter  # type: ignore

        client = GetYuhRates()

        # Prepare parameters
        output_path = None
        writer = None

        if rate_request.save_to_file:
            config_manager = ConfigManager()
            output_folder = config_manager.get_value("output_folder", "./reports/")
            output_path = Path(output_folder)
            output_path.mkdir(parents=True, exist_ok=True)
            writer = CSVWriter()

        # Make the API call
        results = await client.get_rates_async(
            source=rate_request.source,
            currencies=rate_request.currencies,
            output_path=output_path if rate_request.save_to_file else None,
            writer=writer
        )

        return results  # type: ignore

    except ImportError as e:
        raise HTTPException(
            status_code=500,
            detail=f"GetYuhRates package not available: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching rates: {str(e)}"
        )
