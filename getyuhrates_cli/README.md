# GetYuhRates CLI

A command-line interface tool for retrieving currency exchange rates using the GetYuhRates package and the CurrencyLayer API.

## Overview

The GetYuhRates CLI provides an easy-to-use interface for fetching currency exchange rates. It supports configuration via YAML files, environment variables, and command-line arguments, with command-line arguments taking priority over configuration file values.

## Installation

### Prerequisites

- Python 3.12 or higher
- uv (Python package manager)
- The getyuhrates package installed

### Setup

1. Install the getyuhrates package (for development):
   ```bash
   pip install -e path/to/getyuhrates_package
   ```

2. Install CLI dependencies:
   ```bash
   uv pip install typer pyyaml python-dotenv rich
   ```

3. Create configuration files:
   ```bash
   cp config.yaml.example config.yaml
   cp .env.example .env
   ```

4. Edit `.env` and add your CurrencyLayer API key:
   ```
   CURRENCYLAYER_API_KEY="your-actual-api-key-here"
   ```

5. Edit `config.yaml` to set your default preferences:
   ```yaml
   source:
     - GBP
     - USD

   currencies:
     - BBD
     - EUR
     - CAD
     - PLN

   output_folder: ./reports/
   output_format: CSV
   ```

## Usage

### Display Help

Show all available commands:

```bash
python main.py --help
```

Show help for a specific command:

```bash
python main.py get-rates --help
python main.py config test --help
```

### Test Configuration

Validate your configuration file and environment variables:

```bash
python main.py config test
```

This command will:
- Check if `config.yaml` exists and is valid YAML
- Verify all required fields are present
- Load and verify the `.env` file
- Confirm that `CURRENCYLAYER_API_KEY` is set

Example output:
```
Testing GetYuhRates Configuration

============================================================

Configuration Test Passed!

Found config.yaml at: /path/to/config.yaml
Config file is valid YAML
All required fields are present
  - Source currencies: GBP, USD
  - Target currencies: BBD, EUR, CAD, PLN
  - Output folder: ./reports/
  - Output format: CSV

Found .env file at: /path/to/.env
CURRENCYLAYER_API_KEY is set: abcd...xyz

============================================================
All checks passed successfully!
```

### Get Currency Rates

Fetch exchange rates using configuration file defaults:

```bash
python main.py get-rates
```

Override configuration with command-line arguments:

```bash
# Specify source currencies
python main.py get-rates --source USD --source EUR

# Specify target currencies
python main.py get-rates --currencies GBP --currencies CAD

# Specify output path
python main.py get-rates --output-path ./custom_reports/

# Specify writer type
python main.py get-rates --writer CSV

# Combine multiple options
python main.py get-rates --source USD --currencies EUR --currencies GBP --output-path ./reports/
```

Short-form options:

```bash
python main.py get-rates -s USD -s EUR -c GBP -c CAD -o ./reports/ -w CSV
```

Use a different configuration file:

```bash
python main.py get-rates --config /path/to/custom/config.yaml
```

## Configuration

### config.yaml Structure

The configuration file supports the following fields:

```yaml
# Source currencies (base currencies for conversion)
source:
  - GBP
  - USD

# Target currencies (currencies to convert to)
currencies:
  - BBD
  - EUR
  - CAD
  - PLN

# Whether to always download rates (Y/N)
always_download: N

# Output folder for generated reports
output_folder: ./reports/

# Output format (CSV or PDF)
output_format: CSV

# Email Configuration (for future use)
send_emails: true
sender_email: youremail@mail.com
recipients:
  - user1@mail.com
  - user2@mail.com
subject_title: "Today's Currency Rates"
email_body: "Here are the currency rates for today!"
```

### Environment Variables

The CLI requires the following environment variable to be set in your `.env` file:

- `CURRENCYLAYER_API_KEY`: Your CurrencyLayer API access key

## Project Structure

```
getyuhrates_cli/
├── main.py                  # CLI entry point
├── getyuhrates/            # CLI package modules
│   ├── __init__.py
│   ├── config.py           # Configuration loader
│   └── commands.py         # Command implementations
├── config.yaml             # Configuration file
├── config.yaml.example     # Example configuration
├── .env                    # Environment variables
├── .env.example            # Example environment file
├── pyproject.toml          # Project metadata and dependencies
├── .python-version         # Python version specification
├── README.md              # This file
└── reports/               # Default output directory
```

## Command Reference

### `get-rates`

Fetch currency exchange rates from the CurrencyLayer API.

**Options:**
- `--source`, `-s`: Source currencies (can be specified multiple times)
- `--currencies`, `-c`: Target currencies (can be specified multiple times)
- `--output-path`, `-o`: Output folder path for generated reports
- `--writer`, `-w`: Output writer type (CSV or PDF)
- `--config`: Path to config.yaml file (default: ./config.yaml)

**Behavior:**
- Loads defaults from `config.yaml`
- Command-line arguments override config file values
- Saves output files to the specified output folder
- Displays results in the console with progress indicators

### `config test`

Validate configuration and environment setup.

**Options:**
- `--config`, `-c`: Path to config.yaml file (default: ./config.yaml)
- `--env`, `-e`: Path to .env file (default: ./.env)

**Checks:**
- Config file existence and validity
- Required fields presence
- Environment variable configuration
- API key availability

## Development

### Type Checking

Run basedpyright to check for type errors:

```bash
basedpyright
```

All code is fully typed using Python 3.12 type hints, following best practices and Google-style docstrings.

### Adding New Commands

To add new commands:

1. Add the command function to `getyuhratescli/commands.py`
2. Register the command in `main.py`
3. Update this README with the new command documentation

## Troubleshooting

### "Configuration file not found"

Make sure you've created `config.yaml` from the example:
```bash
cp config.yaml.example config.yaml
```

### "CURRENCYLAYER_API_KEY environment variable is not set"

Create a `.env` file from the example and add your API key:
```bash
cp .env.example .env
# Edit .env and add your API key
```

### "Could not import getyuhrates package"

Install the getyuhrates package:
```bash
pip install -e ../getyuhrates_package
```

## License

See the main project LICENSE file for details.
