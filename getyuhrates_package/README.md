# GetYuhRates Package

A Python package for retrieving currency exchange rates from the CurrencyLayer API with support for multiple source currencies and flexible output formats.

## Features

- Retrieve live currency exchange rates from CurrencyLayer API
- Support for multiple source currencies in a single call
- Synchronous and asynchronous API methods
- Export results to CSV or other formats via pluggable writers
- Type-safe with full type annotations
- Automatic handling of same-currency conversions

## Installation

```bash
pip install getyuhrates
```

Or with uv:

```bash
uv pip install getyuhrates
```

## Configuration

Set your CurrencyLayer API key as an environment variable:

```bash
export CURRENCYLAYER_API_KEY="your_api_key_here"
```

Or use a `.env` file with python-dotenv.

## Quick Start

### Basic Usage (Synchronous)

```python
from getyuhrates import GetYuhRates

# Initialize the client
client = GetYuhRates()

# Get exchange rates
results = client.get_rates(
    source=["USD"],
    currencies=["EUR", "GBP", "CAD"]
)

# Access the results
for result in results:
    if result["success"]:
        print(f"Source: {result['source']}")
        print(f"Rates: {result['rates']}")
```

### Async Usage

```python
import asyncio
from getyuhrates import GetYuhRates

async def get_rates():
    client = GetYuhRates()

    results = await client.get_rates_async(
        source=["USD", "GBP"],
        currencies=["BBD", "EUR"]
    )

    for result in results:
        if result["success"]:
            print(f"{result['source']}: {result['rates']}")

asyncio.run(get_rates())
```

### Export to CSV

```python
from getyuhrates import GetYuhRates
from getyuhrates.csv_writer import CSVWriter

client = GetYuhRates()

# Results will be saved to the specified path
results = client.get_rates(
    source=["USD", "GBP", "EUR"],
    currencies=["BBD"],
    output_path="./output",
    writer=CSVWriter()
)

# Check file location in results
for result in results:
    if result["file_location"]:
        print(f"Saved to: {result['file_location']}")
```

## API Reference

### GetYuhRates Class

#### Methods

##### `get_rates(source, currencies, output_path=None, writer=CSVWriter())`

Synchronously retrieve currency exchange rates.

**Parameters:**
- `source` (list[str]): List of source currencies (e.g., ["USD", "GBP"])
- `currencies` (list[str]): List of target currencies to convert to
- `output_path` (str | os.PathLike | None): Optional path to save results
- `writer` (AbstractWriter): Writer instance for file output (default: CSVWriter)

**Returns:**
- `list[CurrencyResult]`: List of results for each source currency

##### `get_rates_async(source, currencies, output_path=None, writer=CSVWriter())`

Asynchronously retrieve currency exchange rates.

**Parameters:**
Same as `get_rates()`

**Returns:**
- `list[CurrencyResult]`: List of results for each source currency

### CurrencyResult TypedDict

Structure of each result returned:

```python
{
    "success": bool,              # Whether the request succeeded
    "source": str,                # Source currency (e.g., "USD")
    "currencies": list[str],      # Target currencies requested
    "rates": dict[str, float],    # Exchange rates (e.g., {"USDEUR": 0.85})
    "reason": str | None,         # Error reason if success is False
    "file_location": str | None   # Path to saved file if output_path provided
}
```

### Custom Writers

Implement the `AbstractWriter` interface to create custom output formats:

```python
from getyuhrates.writer import AbstractWriter
import os

class CustomWriter(AbstractWriter):
    async def async_write_to_file(
        self,
        data: list[CurrencyResult],
        output_folder: os.PathLike,
        filename: str | None
    ):
        # Your implementation here
        pass
```

## Examples

### Multiple Sources to Single Currency

```python
# Get USD, GBP, and EUR rates to Barbadian Dollar
results = client.get_rates(
    source=["USD", "GBP", "EUR"],
    currencies=["BBD"]
)
```

### Multiple Sources to Multiple Currencies

```python
# Each source will be converted to all specified currencies
results = client.get_rates(
    source=["USD", "EUR"],
    currencies=["GBP", "CAD", "JPY"]
)
# This makes 2 API calls (one per source)
```

### Same-Currency Handling

```python
# If source and currency are the same, returns rate of 1.0
results = client.get_rates(
    source=["USD"],
    currencies=["USD"]
)
# Returns: {"USDUSD": 1.0} without making an API call
```

## How It Works

Since the CurrencyLayer API only supports a single source currency per request, the package automatically:

1. Splits multiple sources into separate API requests
2. Executes requests concurrently (in async mode) for better performance
3. Aggregates results into a unified response format
4. Handles same-currency conversions locally (returns rate of 1.0)

## Requirements

- Python 3.12+
- pyyaml
- python-dotenv

## Development

See the main project [CLAUDE.md](../CLAUDE.md) for development guidelines and coding standards.

## License

[Add your license here]

## Links

- [CurrencyLayer API Documentation](https://currencylayer.com/documentation)
