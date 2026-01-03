"""CSV writer implementation.

This module provides a CSV writer that implements the AbstractWriter interface
to export currency exchange rate data to CSV files.
"""

import csv
import os
from datetime import datetime
from pathlib import Path
from typing import override

from getyuhrates.currencyresult import CurrencyResult
from getyuhrates.writer import AbstractWriter


class CSVWriter(AbstractWriter):
    """CSV file writer for currency exchange rate data.

    This writer exports currency exchange rate data to CSV format with columns
    for source currency, target currency, exchange rate, timestamp, and success status.

    The CSV file will have the following columns:
    - source: Source currency code (e.g., "USD")
    - target: Target currency code (e.g., "EUR")
    - rate: Exchange rate as a float
    - pair: Currency pair in format "SOURCETARGET" (e.g., "USDEUR")
    - timestamp: ISO format timestamp of when the data was written
    - success: Boolean indicating if the API request succeeded
    - reason: Error message if success is False, empty otherwise

    Example:
        >>> writer = CSVWriter()
        >>> results = [
        ...     {
        ...         "success": True,
        ...         "source": "USD",
        ...         "currencies": ["EUR", "GBP"],
        ...         "rates": {"USDEUR": 0.85, "USDGBP": 0.74},
        ...         "reason": None,
        ...         "file_location": None
        ...     }
        ... ]
        >>> filepath = await writer.async_write_to_file(
        ...     data=results,
        ...     output_folder=Path("/tmp"),
        ...     filename="rates.csv"
        ... )
    """

    @override
    async def async_write_to_file(
        self,
        data: list[CurrencyResult],
        output_folder: os.PathLike[str],
        filename: str | None,
    ) -> str:
        """Write currency data to a CSV file asynchronously.

        Creates a CSV file with currency exchange rate data. Each row represents
        a single currency pair conversion. The file includes headers and is
        written with UTF-8 encoding.

        Args:
            data (list[CurrencyResult]): List of currency results to write.
                Each result contains exchange rate data for a single source currency.
            output_folder (os.PathLike[str]): Directory path where the CSV file
                should be written. The directory will be created if it doesn't exist.
            filename (str | None): Name for the CSV file. If None, generates a
                timestamped filename in the format "currency_rates_YYYYMMDD_HHMMSS.csv".

        Returns:
            str: Absolute path to the created CSV file.

        Raises:
            OSError: If there are issues creating the directory or writing the file.
            ValueError: If the data list is empty or contains invalid data.

        Example:
            >>> writer = CSVWriter()
            >>> results = [{"success": True, "source": "USD", ...}]
            >>> filepath = await writer.async_write_to_file(
            ...     data=results,
            ...     output_folder=Path("/tmp/output"),
            ...     filename="rates.csv"
            ... )
            >>> print(filepath)
            /tmp/output/rates.csv
        """
        # Convert to Path for easier handling
        output_path = Path(output_folder)

        # Create output directory if it doesn't exist
        output_path.mkdir(parents=True, exist_ok=True)

        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"currency_rates_{timestamp}.csv"

        # Ensure .csv extension
        if not filename.endswith(".csv"):
            filename = f"{filename}.csv"

        # Full file path
        file_path = output_path / filename

        # Prepare rows for CSV
        rows: list[dict[str, str | float | bool]] = []
        timestamp_str = datetime.now().isoformat()

        for result in data:
            source = result["source"]
            success = result["success"]
            reason = result.get("reason") or ""

            if success and result["rates"]:
                # Add a row for each currency pair
                for pair, rate in result["rates"].items():
                    # Extract target currency from pair (e.g., "USDEUR" -> "EUR")
                    # The pair format is SOURCETARGET, so we remove the source prefix
                    target = pair[len(source) :]

                    rows.append(
                        {
                            "source": source,
                            "target": target,
                            "rate": rate,
                            "pair": pair,
                            "timestamp": timestamp_str,
                            "success": success,
                            "reason": reason,
                        }
                    )
            else:
                # Add a single row indicating failure
                rows.append(
                    {
                        "source": source,
                        "target": "",
                        "rate": 0.0,
                        "pair": "",
                        "timestamp": timestamp_str,
                        "success": success,
                        "reason": reason,
                    }
                )

        # Write CSV file
        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            if rows:
                fieldnames = [
                    "source",
                    "target",
                    "rate",
                    "pair",
                    "timestamp",
                    "success",
                    "reason",
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                # writeheader returns a value we don't need, intentionally ignoring it
                writer.writeheader()
                writer.writerows(rows)
            else:
                # Write header only if no data
                _ = csvfile.write("source,target,rate,pair,timestamp,success,reason\n")

        return str(file_path.absolute())
