"""Abstract base class for file writers.

This module defines the AbstractWriter interface that all writer implementations
must inherit from. Writers are responsible for converting CurrencyResult data
into specific file formats (CSV, PDF, etc.).
"""

import os
from abc import ABC, abstractmethod

from getyuhrates.currencyresult import CurrencyResult


class AbstractWriter(ABC):
    """Abstract base class for writing currency data to files.

    This class defines the interface that all writer implementations must follow.
    Subclasses should implement the async_write_to_file method to handle writing
    data in their specific format (CSV, PDF, JSON, etc.).

    Writers are used by the GetYuhRates class to persist currency exchange rate
    data to disk in various formats.
    """

    @abstractmethod
    async def async_write_to_file(
        self,
        data: list[CurrencyResult],
        output_folder: os.PathLike[str],
        filename: str | None,
    ) -> str:
        """Write currency data to a file asynchronously.

        This method must be implemented by all subclasses to handle writing
        currency exchange rate data to disk in the appropriate format.

        Args:
            data (list[CurrencyResult]): List of currency results to write.
                Each result contains exchange rate data for a single source currency.
            output_folder (os.PathLike[str]): Directory path where the file should
                be written. The directory will be created if it doesn't exist.
            filename (str | None): Name for the output file. If None, the
                implementation should generate an appropriate default filename
                based on the current timestamp or other criteria.

        Returns:
            str: Absolute path to the created file.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
            OSError: If there are issues creating the directory or writing the file.
            ValueError: If the data format is invalid or cannot be written.

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
        raise NotImplementedError("Subclasses must implement async_write_to_file")

    def write_to_file(
        self,
        data: list[CurrencyResult],
        output_folder: os.PathLike[str],
        filename: str | None,
    ) -> str:
        """Write currency data to a file synchronously.

        This is a synchronous wrapper around async_write_to_file. It runs the
        async method in an event loop to provide a blocking interface for
        synchronous code.

        Args:
            data (list[CurrencyResult]): List of currency results to write.
            output_folder (os.PathLike[str]): Directory path where the file should
                be written.
            filename (str | None): Name for the output file, or None for default.

        Returns:
            str: Absolute path to the created file.

        Raises:
            OSError: If there are issues creating the directory or writing the file.
            ValueError: If the data format is invalid or cannot be written.

        Example:
            >>> writer = CSVWriter()
            >>> results = [{"success": True, "source": "USD", ...}]
            >>> filepath = writer.write_to_file(
            ...     data=results,
            ...     output_folder=Path("/tmp/output"),
            ...     filename="rates.csv"
            ... )
        """
        import asyncio

        return asyncio.run(self.async_write_to_file(data, output_folder, filename))
