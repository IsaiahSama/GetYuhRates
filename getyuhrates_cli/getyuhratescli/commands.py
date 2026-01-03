"""CLI commands for GetYuhRates.

This module contains the implementation of all CLI commands.
"""

import time
from pathlib import Path

import typer
from rich import print as rprint
from rich.console import Console

from getyuhratescli.config import (
    get_rate_limit_config,
    load_config,
    load_env_file,
    validate_config,
)
from getyuhratescli.rate_limiter import RateLimiter

console = Console()
config_app = typer.Typer(help="Configuration management commands")


@config_app.command("test")
def test_config(
    config_path: Path = typer.Option(
        Path.cwd() / "config.yaml",
        "--config",
        "-c",
        help="Path to config.yaml file",
    ),
    env_path: Path = typer.Option(
        Path.cwd() / ".env",
        "--env",
        "-e",
        help="Path to .env file",
    ),
) -> None:
    """Test and validate configuration files.

    Validates that config.yaml exists, is valid YAML, contains all required fields,
    and that the CURRENCYLAYER_API_KEY environment variable is set.

    Args:
        config_path: Path to config.yaml file.
        env_path: Path to .env file.

    Returns:
        None: Prints validation results to console.
    """
    rprint("\n[bold blue]Testing GetYuhRates Configuration[/bold blue]\n")
    rprint("=" * 60)

    success, message = validate_config(config_path, env_path)

    if success:
        rprint("\n[bold green]Configuration Test Passed![/bold green]\n")
        rprint(message)
        rprint("\n" + "=" * 60)
        rprint("[bold green]All checks passed successfully![/bold green]\n")
    else:
        rprint("\n[bold red]Configuration Test Failed![/bold red]\n")
        rprint(message)
        rprint("\n" + "=" * 60)
        rprint("[bold red]Please fix the errors above and try again.[/bold red]\n")
        raise typer.Exit(code=1)


def get_rates_command(
    source: list[str] | None = typer.Option(
        None,
        "--source",
        "-s",
        help="Source currencies (e.g., USD, GBP). Can be specified multiple times.",
    ),
    currencies: list[str] | None = typer.Option(
        None,
        "--currencies",
        "-c",
        help="Target currencies (e.g., EUR, CAD). Can be specified multiple times.",
    ),
    output_path: Path | None = typer.Option(
        None,
        "--output-path",
        "-o",
        help="Output folder path for generated reports",
    ),
    writer: str | None = typer.Option(
        None,
        "--writer",
        "-w",
        help="Output writer type (CSV or PDF)",
    ),
    config_path: Path = typer.Option(
        Path.cwd() / "config.yaml",
        "--config",
        help="Path to config.yaml file",
    ),
    no_rate_limit: bool = typer.Option(
        False,
        "--no-rate-limit",
        help="Bypass rate limiting for API requests",
    ),
) -> None:
    """Get currency exchange rates from CurrencyLayer API.

    Retrieves exchange rates using parameters from config.yaml by default.
    Command-line arguments override config file values.

    Args:
        source: List of source currencies. If None, uses config file values.
        currencies: List of target currencies. If None, uses config file values.
        output_path: Output folder path. If None, uses config file value.
        writer: Output writer type. If None, uses config file value.
        config_path: Path to config.yaml file.
        no_rate_limit: If True, bypasses rate limiting for API requests.

    Returns:
        None: Writes output files and prints results to console.
    """
    # Load environment variables
    load_env_file()

    # Load configuration
    try:
        config = load_config(config_path)
    except Exception as e:
        rprint(f"[bold red]Error loading configuration:[/bold red] {e}")
        raise typer.Exit(code=1)

    # Override config with command-line arguments
    final_source = source if source is not None else config["source"]
    final_currencies = currencies if currencies is not None else config["currencies"]
    final_output_path = (
        str(output_path) if output_path is not None else config["output_folder"]
    )
    final_writer = writer if writer is not None else config["output_format"]

    # Get rate limit configuration
    rate_limit_config = get_rate_limit_config(config)

    # Create rate limiter if enabled and not bypassed
    rate_limiter: RateLimiter | None = None
    if rate_limit_config["enabled"] and not no_rate_limit:
        rate_limiter = RateLimiter(
            delay_seconds=rate_limit_config["delay_seconds"],
            respect_headers=rate_limit_config["respect_headers"],
        )
        rprint(
            f"[dim]Rate limiting enabled: {rate_limit_config['delay_seconds']}s delay between requests[/dim]"
        )
    elif no_rate_limit:
        rprint("[dim yellow]Rate limiting bypassed via --no-rate-limit flag[/dim yellow]")

    # Display configuration
    rprint("\n[bold blue]GetYuhRates - Fetching Currency Rates[/bold blue]\n")
    rprint("=" * 60)
    rprint(f"[cyan]Source currencies:[/cyan] {', '.join(final_source)}")
    rprint(f"[cyan]Target currencies:[/cyan] {', '.join(final_currencies)}")
    rprint(f"[cyan]Output path:[/cyan] {final_output_path}")
    rprint(f"[cyan]Writer type:[/cyan] {final_writer}")
    rprint("=" * 60 + "\n")

    try:
        # Import the getyuhrates package
        # Note: We're ignoring type errors here as the package is still in development
        from getyuhrates import GetYuhRates  # type: ignore[import-not-found]
        from getyuhrates.csv_writer import CSVWriter  # type: ignore[import-not-found]

        # Initialize the client
        client = GetYuhRates()

        # Determine writer instance
        if final_writer.upper() == "CSV":
            writer_instance = CSVWriter()
        else:
            rprint(
                f"[bold yellow]Warning:[/bold yellow] {final_writer} writer not yet implemented, using CSV"
            )
            writer_instance = CSVWriter()

        # Fetch rates for each source currency with rate limiting
        rprint("[bold]Fetching rates...[/bold]\n")
        results = []

        for idx, source_currency in enumerate(final_source):
            # Apply rate limiting before each API call (except the first one)
            if rate_limiter is not None and idx > 0:
                rate_limiter.wait_if_needed()

            rprint(f"[cyan]Fetching rates for {source_currency}...[/cyan]")

            # Call get_rates for this specific source
            source_results = client.get_rates(
                source=[source_currency],
                currencies=final_currencies,
                output_path=final_output_path,
                writer=writer_instance,
            )

            # If rate limiter is enabled and we got results, try to extract headers
            # Note: This assumes the API client might provide response metadata
            # Since we don't have direct access to response headers from the package,
            # we'll skip header-based rate limiting for now. The delay-based limiting
            # will still work.
            if rate_limiter is not None:
                # Update last request time after successful call
                rate_limiter.last_request_time = time.time()

            results.extend(source_results)

        # Display results
        rprint("\n[bold green]Results:[/bold green]\n")
        for result in results:
            if result["success"]:
                rprint(f"[green]Success:[/green] {result['source']}")
                if result.get("file_location"):
                    rprint(f"  [dim]File saved to: {result['file_location']}[/dim]")
            else:
                rprint(f"[red]Failed:[/red] {result['source']}")
                if result.get("reason"):
                    rprint(f"  [dim]Reason: {result['reason']}[/dim]")

        rprint("\n[bold green]Done![/bold green]\n")

    except ImportError as e:
        rprint(f"[bold red]Error:[/bold red] Could not import getyuhrates package: {e}")
        rprint("\nMake sure the getyuhrates package is installed:")
        rprint("  [cyan]pip install -e path/to/getyuhrates_package[/cyan]\n")
        raise typer.Exit(code=1)
    except Exception as e:
        rprint(f"[bold red]Error fetching rates:[/bold red] {e}")
        raise typer.Exit(code=1)
