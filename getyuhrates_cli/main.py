"""GetYuhRates CLI - Main entry point.

This is the main CLI application for GetYuhRates, providing commands to
retrieve currency exchange rates and manage configuration.
"""

import typer

from getyuhratescli.commands import config_app, get_rates_command

app = typer.Typer(
    name="getyuhrates",
    help="GetYuhRates - CLI tool for retrieving currency exchange rates",
    add_completion=False,
)

# Add the config subcommand
app.add_typer(config_app, name="config")

# Add the get_rates command
app.command(name="get-rates")(get_rates_command)


def main() -> None:
    """Main entry point for the CLI application.

    Returns:
        None: Runs the Typer application.
    """
    app()


if __name__ == "__main__":
    main()
