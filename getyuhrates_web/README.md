# GetYuhRates Web Service

A FastAPI-based web application for managing currency exchange rates using the GetYuhRates package.

## Features

- **Get Exchange Rates**: Retrieve live currency exchange rates from the CurrencyLayer API
- **Report Management**: View, download, and delete saved currency rate reports
- **Configuration Management**: Manage application settings through a user-friendly interface
- **Responsive UI**: Clean, professional Bootstrap-based interface

## Prerequisites

- Python 3.12 or higher
- uv (recommended) or pip for package management
- CurrencyLayer API key (get one at [currencylayer.com](https://currencylayer.com))

## Installation

### 1. Install the GetYuhRates Package

First, install the GetYuhRates package as an editable dependency:

```bash
cd /path/to/GetYuhRates
uv pip install -e ./getyuhrates_package
```

Or with pip:

```bash
pip install -e ./getyuhrates_package
```

### 2. Install Web Application Dependencies

```bash
cd getyuhrates_web
uv pip install -e .
```

Or with pip:

```bash
pip install -e .
```

### 3. Configure Environment Variables

Copy the example `.env` file and add your CurrencyLayer API key:

```bash
cp .env.example .env
```

Edit `.env` and set your API key:

```
CURRENCYLAYER_API_KEY="your-api-key-here"
```

### 4. Configure Application Settings

Copy the example configuration file:

```bash
cp config.yaml.example config.yaml
```

Edit `config.yaml` to set your preferences. The default configuration includes:

- **source**: Default source currencies (e.g., GBP, USD)
- **currencies**: Default target currencies (e.g., BBD, EUR, CAD, PLN)
- **always_download**: Whether to always save reports (Y/N)
- **output_folder**: Directory where reports are saved (default: ./reports/)
- **output_format**: File format for reports (CSV or PDF)
- **Email settings**: Configure email notifications (optional)

## Running the Application

### Development Mode

Run with auto-reload enabled:

```bash
fastapi dev main.py
```

Or:

```bash
python main.py
```

The application will be available at [http://localhost:8000](http://localhost:8000)

### Production Mode

Run in production mode:

```bash
fastapi run main.py
```

Or with uvicorn directly:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Usage

### Home Page

The home page provides an overview of the application and shows your most recent reports.

Navigate to: [http://localhost:8000](http://localhost:8000)

### Get Exchange Rates

1. Navigate to the "Get Rates" page
2. Select one or more source currencies (hold Ctrl/Cmd for multiple)
3. Select one or more target currencies
4. Optionally check "Save results to CSV file" to store the results
5. Click "Get Rates"

The results will be displayed on the page, showing exchange rates for all currency pairs.

### Manage Reports

Navigate to the "Reports" page to:

- View all saved reports
- Download reports to your computer
- Delete old reports

### Configure Settings

Navigate to the "Settings" page to:

- Set default source and target currencies
- Configure output format (CSV or PDF)
- Set up email notifications
- Adjust other application settings

Note: The `output_folder` setting cannot be modified through the web interface for security reasons.

## Project Structure

```
getyuhrates_web/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application definition
│   ├── config.py            # Configuration management utilities
│   ├── models/
│   │   ├── __init__.py
│   │   ├── requests.py      # Pydantic request models
│   │   └── responses.py     # Pydantic response models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── home.py          # Home page routes
│   │   ├── rates.py         # Currency rates routes
│   │   ├── reports.py       # Report management routes
│   │   └── config.py        # Configuration routes
│   └── templates/
│       ├── base.html        # Base template
│       ├── index.html       # Home page
│       ├── rates.html       # Get rates page
│       ├── reports.html     # Reports management page
│       └── config.html      # Settings page
├── reports/                  # Saved reports directory
├── main.py                   # Entry point
├── config.yaml               # Application configuration
├── .env                      # Environment variables
├── pyproject.toml            # Project dependencies
└── README.md                 # This file
```

## API Endpoints

The application provides both HTML pages and JSON API endpoints:

### HTML Pages

- `GET /` - Home page
- `GET /rates` - Currency rates page
- `GET /reports` - Reports management page
- `GET /config` - Configuration page

### API Endpoints

- `POST /rates/fetch` - Fetch currency rates (JSON)
- `GET /reports/list` - List all reports (JSON)
- `GET /reports/download/{filename}` - Download a report file
- `DELETE /reports/delete/{filename}` - Delete a report
- `GET /config/data` - Get current configuration (JSON)
- `POST /config/update` - Update configuration (JSON)

## Development

### Type Checking

Run basedpyright to check types:

```bash
basedpyright
```

### Testing

(Tests to be added following TDD principles)

```bash
pytest
```

## Common Issues

### API Key Not Set

If you see "CURRENCYLAYER_API_KEY not configured", make sure you:

1. Created the `.env` file from `.env.example`
2. Set a valid API key in the `.env` file
3. Restarted the application after setting the key

### Config File Not Found

If you see "Configuration file not found", make sure you:

1. Created `config.yaml` from `config.yaml.example`
2. The file is in the `getyuhrates_web` directory

### Package Import Errors

If you see "GetYuhRates package not available", make sure you:

1. Installed the getyuhrates package as an editable dependency
2. Activated the correct virtual environment

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Jinja2**: Template engine for HTML rendering
- **Bootstrap 5**: CSS framework for responsive UI
- **uvicorn**: ASGI server for running the application
