# Project Overview

This project is called `GetYuhRates`, and is a three (3) component program, designed to primarily retrieve configurable Currency rates via the CurrencyLayer API, and then display the information in an aggregated manner, such as PDF or CSV.

# Project Structure

This project contains three (3) sets of code.

1. CL Package: The core functionality responsible for interacting with the Currency Layer API, as a Python package designed to be installed and imported.
1. CLI Tool: A Python CLI program developed using Typer, that uses the developed package.
1. Web Application: Web Application developed using FastAPI, that uses the developed package, and a user interface to configuration settings.

The GetYuhRates package, will be stored in the `./getyuhrates_package` directory.
The CLI tool will be stored in the `./getyuhrates_cli` directory.
The Web application will be stored in the `./getyuhrates_web/` directory.

Each of these projects will also have their own `CLAUDE.md` file containing information specific to that project.

# Running the Projects

Refer to the README in each project for information on how the project should be run.

# Tools Used

In development, the following tools will be used:

## Global

- FISH shell
- Python 3.12
- uv
- git
- basedpyright
- pyyaml
- python-dotenv

## CLI Tool

- Typer

## Web Application

- FastAPI
- Pydantic

# Coding Guidelines

All Python code should be `typed`, avoiding the use of `Any` whenever possible.
All Python functions & modules should be documented using Google style docstrings. For example:

```py
def some_func(name: str) -> None:
    """One line summary

    Args:
        name (str): One line summary.

    Returns:
        None: One line reason
    """
    pass
```

# Workflow

- When you change code, use `basedpyright` to run the typechecker
- Before adding a new feature, follow Test Driven Development, and create a test first.
- Adhere to the provided specifications for each project. If an improvement or deviation must be made, then document it in a `CLAUDE_CHANGES.md` file in the directory where the changes are made.
