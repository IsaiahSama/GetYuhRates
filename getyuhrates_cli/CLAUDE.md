# Get Yuh Rates CLI

This folder contains the code for the `GetYuhRates` CLI tool.
This acts as a wrapper around the `getyuhrates` package, providing an easy to use interface.
The CLI tool will be built using the Typer python library.

Each command for the CLI will by default use the appropriate arguments loaded from the `config.yaml` file.

However, the commands will still retain support for command line arguments as well, which will take priority over values loaded from the `config.yaml` file.

Note, for development, the `getyuhrates` package should be installed using `pip install -e path/to/package`

## Project Structure

The root folder will contain:

- README.md
- main.py: Entry point to the application.
- .python-version: File containing the python version being used.
- pyproject.toml: Meta information about the CLI tool.
- getyuhrates/: Folder containing code used by the CLI tool.
- `getyuhrates/__init__.py`
- .env.example: Example environment file.
- .env: Environment file.
- config.yaml.example: Example config file.
- config.yaml: Configuration file for the service.
- reports/: Default folder for storing generated reports

## Commands

The CLI tool should provide the following commands:

- `help`: Display a list of the available commands and what they do. This should rely on Typer's internal functionality.
- `get_rates source currencies output_path writer`: Queries the API for rates either from the config file, or from provied arguments
- `config test`: Ensures the config file exists, is valid, and has all fields. This should also load environment variables, and ensure that CURRENCYLAYER_API_KEY is set.


