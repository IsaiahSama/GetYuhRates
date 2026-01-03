# Get Yuh Rates Package

This folder contains the core functionality for the Get Yuh Rates package, which will interact with the Currency Layer API, along with provide methods for generating a CSV or PDF file.

## Project Structure

The project should be structured as follows:

At the root (this folder), we have:

- README.md: Readme file containing information about the package.
- .python-version: File containing the python version being used.
- pyproject.toml: Information about the package.
- src/: Directory for the code.
- src/getyuhrates/: Directory where the code for the package will be written.
- tests/: Directory for tests that test the package.

Inside of the `src/getyuhrates/`, there should be the following files:

- `__init__.py`
- `getyuhrates.py`: Main module containing the GetYuhRates class.
- `currencyresult.py`: Class representing a success / failure operation for data retrieval.
- `writer.py`: File holding an `AbstractWriter` class. 
- `csv_writer.py`: File holding CSV Writer class that inherits from the `AbstractWriter` class.

## Code Structure

The code will be inside of the `./src/getyuhrates/getyuhrates.py` file.
This will consist of a class called `GetYuhRates`, containing async and sync methods for interacting with the CurrencyLayer API.

For example:

```py

class GetYuhRates:

    async def get_rates_async(source: list[str], currencies: list[str], output_path: str | os.PathLike | None = None, writer: AbstractWriter = CSVWriter()):
        pass

    def get_rates(source: list[str], currencies: list[str], output_path: str | os.PathLike | None = None, writer: AbstractWriter = CSVWriter()):
        pass
```

This will also have an async and sync method for creating a CSV file with the retrieved data.

`./src/getyuhrates/currencyresult.py` will be a TypedDict with the following structure:

```py

class CurrencyResult(TypedDict):
    success: bool
    source: str # The source currency
    currencies: list[str] # List of currencies source was mapped to.
    rates: dict[str, float] # Mapping of currency names to their rates. Example: { "USDEUR":0.852504, "USDGBP":0.742556, "USDCAD":1.37365 }
    reason: str | None # Reason why the request failed.
    file_location: str | None # Location where file was stored, if this option was selected.
```

`./src/getyuhrates/writer.py` will have an abstract class declaring functionality a writer will have. For example:

```py

class AbstractWriter(ABC):
    
    @abstractmethod
    async def async_write_to_file(data: list[CurrencyResult], output_folder: os.PathLike, filename: str | None):
        raise NotImplementedError
```

## API Structure

This project will primarily support the `live` route of the CurrencyLayer API.

The url for this route is: `https://apilayer.net/api/live`.
The route takes the following parameters:

- `access_key`: Currency Layer access key retrieved from a set environment variable called CURRENCYLAYER_API_KEY.
- `source`: A **single** currency to use as a base.
- `currencies`: List of currencies to query the exchange rate compared to the base.
- `format`: Integer with a value of 0 or 1. This should always be set to 1.

## Key Considerations

Given that users may want to have multiple sources, for example, getting a list of currency conversions as follows:

- USDBBD
- GBPBBD
- EURBBD

Then the sources will be `[USD, GBP, EUR]` and the `currencies` will be `[BBD]`. However, the API does NOT support multiple sources. Therefore this will need to be split into three (3) different requests. The sync and async methods for making these requests should automatically consider that.

If multiple a list is provided for `source` and for `currencies`, then for each `source` the service should make a request for the `currencies`.

If at any point, the source and the currency is the exact same, then skip it and return a rate of `1`.
However, if the source is also included alongside a list of other currencies, then make the request as normal, since the CurrencyLayer API will handle it appropriately, returning no value for that entry.
