"""GetYuhRates - Currency exchange rate retrieval package.

This package provides an interface for retrieving live currency exchange rates
from the CurrencyLayer API with support for multiple source currencies and
flexible output formats.

Main exports:
    GetYuhRates: Main client class for API interactions
    CurrencyResult: TypedDict for result data structure
    AbstractWriter: Base class for implementing custom writers
    CSVWriter: CSV file writer implementation

Example:
    >>> from getyuhrates import GetYuhRates
    >>> client = GetYuhRates()
    >>> results = client.get_rates(source=["USD"], currencies=["EUR", "GBP"])
    >>> print(results[0]["rates"])
"""

from getyuhrates.csv_writer import CSVWriter
from getyuhrates.currencyresult import CurrencyResult
from getyuhrates.getyuhrates import GetYuhRates
from getyuhrates.writer import AbstractWriter

__all__ = [
    "GetYuhRates",
    "CurrencyResult",
    "AbstractWriter",
    "CSVWriter",
]

__version__ = "0.1.0"
