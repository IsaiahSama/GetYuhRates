# GetYuhRates

GetYuhRates is an automation driven script, designed to be run once daily automatically, to retrieve a configurable set of currency exchange rates, and aggregate them into an easy to view format such as PDF or CSV file. These files can then be downloaded, or be configured to be sent to a group of emails automatically.

This consists of three (3) folders:

- getyuhrates_web/
- getyuhrates_cli/
- getyuhrates_package/

Where:

- getyuhrates_web/ contains a deployable website to interact with the service via a user interface
- getyuhrates_cli/ contains a command line tool, that allows you to interact with the service, and run direct commands. This is the ideal method of using the service.
- getyuhrates_package/ contains the core functionality of the service that will be used by the CLI and Web Application.

NOTE: This project will require a Python installation to run.

## Using the Service

This service has some external dependencies that will require you to set up before you can use it.
These include:

- Acquiring a free API key from [Currency Layer](https://currencylayer.com/).
- [OPTIONAL]: Setting up Google Credentials. This is if you want the emails to be sent.

### How to use Web Application

To use the Web application for this project, follow the following steps:

1. Ensure Python 3.11 or later is installed on the system.
1. From the root (this folder), use `cd ./getyuhrates_web/`
1. [OPTIONAL]: Create a virtual environment with `python -m venv .venv` and activate with `source .venv/bin/activate` or `source .venv/Scripts/Activate`
1. Install the dependencies with `pip install -r requirements.txt`
1. Run: `cp .env.example .env` and fill in the `CURRENCYLAYER_API_KEY` value with your Currency Layer API Key.
1. Run the server with `fastapi run main.py`
1. Visit [the page](http://127.0.0.1:8000)
1. Here, you can create and modify the configuration of the service.

### How to use the CLI tool

The CLI tool can be used as follows:

1. Ensure Python 3.11 or later is installed on the system.
1. From the root (this folder), use `cd ./getyuhrates_cli/`
1. [OPTIONAL]: Create a virtual environment with `python -m venv .venv` and activate with `source .venv/bin/activate` or `source .venv/Scripts/Activate`
1. Install the dependencies with `pip install -r requirements.txt`
1. Run: `cp .env.example .env` and fill in the `CURRENCYLAYER_API_KEY` value with your Currency Layer API Key.
1. Run: `cp config.yaml.example config.yaml` to copy the config file. Following the established format, make any changes you want.
1. Run `main --help` for a list of available commands.


