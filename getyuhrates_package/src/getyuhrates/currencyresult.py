"""Currency result type definition.

This module defines the CurrencyResult TypedDict structure used throughout
the getyuhrates package to represent the results of currency exchange rate queries.
"""

from typing import TypedDict


class CurrencyResult(TypedDict):
    """Result structure for currency exchange rate operations.

    This TypedDict defines the standard format for returning currency exchange
    rate data from the CurrencyLayer API, including success status, rates, and
    optional file location if results were written to disk.

    Attributes:
        success (bool): Whether the API request succeeded.
        source (str): The source currency code (e.g., "USD", "GBP").
        currencies (list[str]): List of target currency codes that were requested.
        rates (dict[str, float]): Mapping of currency pairs to their exchange rates.
            Keys are in the format "SOURCETARGET" (e.g., "USDEUR" for USD to EUR).
            Values are the exchange rates as floats.
        reason (str | None): Error message if the request failed, None otherwise.
        file_location (str | None): Absolute path to the output file if results
            were written to disk, None otherwise.

    Example:
        >>> result: CurrencyResult = {
        ...     "success": True,
        ...     "source": "USD",
        ...     "currencies": ["EUR", "GBP", "CAD"],
        ...     "rates": {
        ...         "USDEUR": 0.852504,
        ...         "USDGBP": 0.742556,
        ...         "USDCAD": 1.37365
        ...     },
        ...     "reason": None,
        ...     "file_location": "/path/to/output/rates.csv"
        ... }
    """

    success: bool
    source: str
    currencies: list[str]
    rates: dict[str, float]
    reason: str | None
    file_location: str | None
