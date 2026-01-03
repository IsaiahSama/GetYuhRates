# Get Yuh Rates Web Service

This is a webservice developed using Fast API, that will make use of the `getyuhrates` package.

For development, this package should be installed using `pip install -e path/to/package`.

The aim of this is to provide a nice user interface for:

- Making requests to Currency Layer
- Storing the reports as files in a `reports/` directory, and allowing the user to manage them from the website.
- Change most values within the `config.yaml`. The only value that will not be changed is `output_folder`.

This will provide appropriate, friendly dropdowns and similar conveniences wherever applicable.

## Project Structure

The root folder (this folder) will have:

- .env.example: Example environment file
- config.yaml.example: Example configuration file.
- README.md: README file
- main.py: Entry point to fastapi application, to be run with `fastapi run main.py`
- .python-version: Version of python used
- pyproject.toml: Information about the package.
- app/: Directory where application code will be stored.
- .env: Actual environment file
- config.yaml: Actual configuration file

The app directory will be where all of the code for the server is actually stored. 
Example structure:

- `app/`
- `app/templates/`: Directory where templates are stored
- `app/main.py`: Where FastAPI application is defined
- `app/routes/`: Directory where the routes are declared.
- `app/models/`: Directory where any app specific models are stored.
- `app/__init__.py`

## Project Guidelines

This application should follow FastAPI best practices, including using Pydantic, Strong typing, lifetimes (where necessary), and modular directory structure.

