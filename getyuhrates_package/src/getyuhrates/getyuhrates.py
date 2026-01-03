"""Main GetYuhRates class for retrieving currency exchange rates.

This module provides the primary interface for interacting with the CurrencyLayer
API to retrieve live currency exchange rates. It supports both synchronous and
asynchronous operations, handles multiple source currencies, and can export
results to various file formats.
"""

import asyncio
import os
from typing import Any, cast

import aiohttp
import requests
from dotenv import load_dotenv

from getyuhrates.csv_writer import CSVWriter
from getyuhrates.currencyresult import CurrencyResult
from getyuhrates.writer import AbstractWriter

# Load environment variables from .env file
_ = load_dotenv()


class GetYuhRates:
    """Client for retrieving currency exchange rates from CurrencyLayer API.

    This class provides methods to fetch live currency exchange rates from the
    CurrencyLayer API. It supports multiple source currencies, automatic request
    splitting (since the API only supports one source per request), and optional
    file output in various formats.

    The API key is retrieved from the CURRENCYLAYER_API_KEY environment variable.

    Attributes:
        api_key (str): CurrencyLayer API key from environment.
        base_url (str): Base URL for the CurrencyLayer API.

    Example:
        >>> client = GetYuhRates()
        >>> results = client.get_rates(
        ...     source=["USD", "GBP"],
        ...     currencies=["EUR", "CAD"]
        ... )
        >>> for result in results:
        ...     if result["success"]:
        ...         print(f"{result['source']}: {result['rates']}")
    """

    def __init__(self) -> None:
        """Initialize the GetYuhRates client.

        Loads the API key from the CURRENCYLAYER_API_KEY environment variable.

        Raises:
            ValueError: If the CURRENCYLAYER_API_KEY environment variable is not set.
        """
        self.api_key: str | None = os.getenv("CURRENCYLAYER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "CURRENCYLAYER_API_KEY environment variable is not set. Please set it with your CurrencyLayer API key."
            )
        self.base_url: str = "https://apilayer.net/api/live"

    async def get_rates_async(
        self,
        source: list[str],
        currencies: list[str],
        output_path: str | os.PathLike[str] | None = None,
        writer: AbstractWriter | None = None,
    ) -> list[CurrencyResult]:
        """Retrieve currency exchange rates asynchronously.

        Fetches live currency exchange rates from the CurrencyLayer API for
        multiple source currencies. Requests are made concurrently for better
        performance. If source and target currency are identical, returns a
        rate of 1.0 without making an API call.

        Args:
            source (list[str]): List of source currency codes (e.g., ["USD", "GBP"]).
                Each source will result in a separate API request.
            currencies (list[str]): List of target currency codes to get rates for
                (e.g., ["EUR", "CAD", "JPY"]). Applied to all source currencies.
            output_path (str | os.PathLike[str] | None): Optional directory path
                to save results. If provided, results will be written using the
                specified writer. Default is None (no file output).
            writer (AbstractWriter | None): Writer instance for file output.
                Default is CSVWriter if None provided and output_path is set.

        Returns:
            list[CurrencyResult]: List of results, one per source currency.
                Each result contains success status, rates, and optional file location.

        Raises:
            ValueError: If source or currencies lists are empty.
            aiohttp.ClientError: If there are network issues with the API request.

        Example:
            >>> client = GetYuhRates()
            >>> results = await client.get_rates_async(
            ...     source=["USD", "GBP"],
            ...     currencies=["EUR", "BBD"],
            ...     output_path="/tmp/output"
            ... )
            >>> for result in results:
            ...     print(f"{result['source']}: {result['rates']}")
        """
        if not source:
            raise ValueError("Source currency list cannot be empty")
        if not currencies:
            raise ValueError("Target currencies list cannot be empty")

        # Use CSVWriter as default if output_path is provided but no writer is specified
        if output_path and writer is None:
            writer = CSVWriter()

        # Create tasks for each source currency
        tasks = [
            self._fetch_rates_async(src, currencies) for src in source
        ]

        # Execute all requests concurrently
        results = await asyncio.gather(*tasks)

        # Write to file if output path is provided
        if output_path and writer:
            file_path = await writer.async_write_to_file(
                data=results,
                output_folder=cast(os.PathLike[str], output_path),
                filename=None,
            )
            # Update all results with the file location
            for result in results:
                result["file_location"] = file_path

        return results

    async def _fetch_rates_async(
        self, src: str, currencies: list[str]
    ) -> CurrencyResult:
        """Fetch rates for a single source currency asynchronously.

        Internal method that handles API requests for a single source currency.
        If the source currency equals all target currencies, returns a rate of
        1.0 without making an API call.

        Args:
            src (str): Source currency code.
            currencies (list[str]): List of target currency codes.

        Returns:
            CurrencyResult: Result containing rates and status information.
        """
        # Check if source equals all currencies (skip API call)
        if len(currencies) == 1 and src == currencies[0]:
            return {
                "success": True,
                "source": src,
                "currencies": currencies,
                "rates": {f"{src}{src}": 1.0},
                "reason": None,
                "file_location": None,
            }

        # Build API request parameters
        # Note: self.api_key is guaranteed to be str (not None) due to __init__ validation
        params: dict[str, str | int] = {
            "access_key": cast(str, self.api_key),
            "source": src,
            "currencies": ",".join(currencies),
            "format": 1,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    # Using Any here is necessary because the API response structure is dynamic
                    # and cannot be fully typed without creating complex type definitions
                    data: dict[str, Any] = await response.json()

                    if data.get("success"):
                        # Cast to the expected type after validation
                        quotes: dict[str, float] = cast(dict[str, float], data.get("quotes", {}))
                        return {
                            "success": True,
                            "source": src,
                            "currencies": currencies,
                            "rates": quotes,
                            "reason": None,
                            "file_location": None,
                        }
                    else:
                        # Extract error information with proper casting
                        error_info: dict[str, Any] = cast(dict[str, Any], data.get("error", {}))
                        error_msg: str = str(error_info.get("info", "Unknown error"))
                        return {
                            "success": False,
                            "source": src,
                            "currencies": currencies,
                            "rates": {},
                            "reason": error_msg,
                            "file_location": None,
                        }
        except Exception as e:
            return {
                "success": False,
                "source": src,
                "currencies": currencies,
                "rates": {},
                "reason": f"Request failed: {str(e)}",
                "file_location": None,
            }

    def get_rates(
        self,
        source: list[str],
        currencies: list[str],
        output_path: str | os.PathLike[str] | None = None,
        writer: AbstractWriter | None = None,
    ) -> list[CurrencyResult]:
        """Retrieve currency exchange rates synchronously.

        Fetches live currency exchange rates from the CurrencyLayer API for
        multiple source currencies. This is a synchronous wrapper around
        get_rates_async that runs the async method in an event loop.

        Args:
            source (list[str]): List of source currency codes (e.g., ["USD", "GBP"]).
            currencies (list[str]): List of target currency codes (e.g., ["EUR", "CAD"]).
            output_path (str | os.PathLike[str] | None): Optional directory path
                to save results. Default is None (no file output).
            writer (AbstractWriter | None): Writer instance for file output.
                Default is CSVWriter if None provided and output_path is set.

        Returns:
            list[CurrencyResult]: List of results, one per source currency.

        Raises:
            ValueError: If source or currencies lists are empty.
            requests.RequestException: If there are network issues with the API request.

        Example:
            >>> client = GetYuhRates()
            >>> results = client.get_rates(
            ...     source=["USD"],
            ...     currencies=["EUR", "GBP", "CAD"],
            ...     output_path="./output"
            ... )
            >>> print(results[0]["rates"])
            {'USDEUR': 0.85, 'USDGBP': 0.74, 'USDCAD': 1.37}
        """
        return asyncio.run(
            self.get_rates_async(source, currencies, output_path, writer)
        )

    def _fetch_rates_sync(self, src: str, currencies: list[str]) -> CurrencyResult:
        """Fetch rates for a single source currency synchronously.

        Internal method that handles API requests for a single source currency
        using the requests library. If the source currency equals all target
        currencies, returns a rate of 1.0 without making an API call.

        This method is kept for potential future use but currently the package
        uses the async method with asyncio.run() for the synchronous interface.

        Args:
            src (str): Source currency code.
            currencies (list[str]): List of target currency codes.

        Returns:
            CurrencyResult: Result containing rates and status information.
        """
        # Check if source equals all currencies (skip API call)
        if len(currencies) == 1 and src == currencies[0]:
            return {
                "success": True,
                "source": src,
                "currencies": currencies,
                "rates": {f"{src}{src}": 1.0},
                "reason": None,
                "file_location": None,
            }

        # Build API request parameters
        # Note: self.api_key is guaranteed to be str (not None) due to __init__ validation
        params: dict[str, str | int] = {
            "access_key": cast(str, self.api_key),
            "source": src,
            "currencies": ",".join(currencies),
            "format": 1,
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            # Using Any here is necessary because the API response structure is dynamic
            # and cannot be fully typed without creating complex type definitions
            data: dict[str, Any] = response.json()

            if data.get("success"):
                # Cast to the expected type after validation
                quotes: dict[str, float] = cast(dict[str, float], data.get("quotes", {}))
                return {
                    "success": True,
                    "source": src,
                    "currencies": currencies,
                    "rates": quotes,
                    "reason": None,
                    "file_location": None,
                }
            else:
                # Extract error information with proper casting
                error_info: dict[str, Any] = cast(dict[str, Any], data.get("error", {}))
                error_msg: str = str(error_info.get("info", "Unknown error"))
                return {
                    "success": False,
                    "source": src,
                    "currencies": currencies,
                    "rates": {},
                    "reason": error_msg,
                    "file_location": None,
                }
        except Exception as e:
            return {
                "success": False,
                "source": src,
                "currencies": currencies,
                "rates": {},
                "reason": f"Request failed: {str(e)}",
                "file_location": None,
            }
