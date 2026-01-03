"""Rate limiting module for GetYuhRates CLI.

This module provides rate limiting functionality to prevent excessive API requests
and respect API rate limits based on response headers.
"""

import time
from datetime import datetime, timezone

from rich.console import Console


class RateLimiter:
    """Manages API rate limiting with configurable delays and header awareness.

    This class tracks the timing of API requests and enforces delays between
    consecutive requests. It can also adjust delays dynamically based on API
    response headers indicating rate limit status.

    Attributes:
        delay_seconds: Time to wait between requests in seconds.
        respect_headers: Whether to check and adjust based on API response headers.
        last_request_time: Timestamp of the last API request.
        console: Rich console for displaying progress messages.
    """

    def __init__(self, delay_seconds: float, respect_headers: bool = True) -> None:
        """Initialize rate limiter.

        Args:
            delay_seconds: Time to wait between requests in seconds.
            respect_headers: Whether to check API response headers for rate limit info.

        Returns:
            None: Initializes the rate limiter instance.
        """
        self.delay_seconds = delay_seconds
        self.respect_headers = respect_headers
        self.last_request_time: float | None = None
        self.console = Console()
        self._dynamic_delay: float | None = None

    def wait_if_needed(self) -> None:
        """Wait according to rate limit rules before making the next request.

        This method should be called before each API request. It calculates
        how much time has elapsed since the last request and sleeps for the
        remaining time to respect the configured delay.

        Returns:
            None: Blocks execution until the rate limit delay is satisfied.
        """
        current_time = time.time()

        # If this is not the first request, enforce the delay
        if self.last_request_time is not None:
            elapsed = current_time - self.last_request_time

            # Use dynamic delay if set, otherwise use configured delay
            required_delay = self._dynamic_delay if self._dynamic_delay is not None else self.delay_seconds

            if elapsed < required_delay:
                wait_time = required_delay - elapsed
                self.console.print(
                    f"[dim cyan]Rate limit: waiting {wait_time:.1f}s before next request[/dim cyan]"
                )
                time.sleep(wait_time)

        # Update last request time
        self.last_request_time = time.time()

    def update_from_headers(self, headers: dict[str, str]) -> None:
        """Update rate limit settings based on API response headers.

        Examines common rate limit headers (X-RateLimit-Remaining, X-RateLimit-Reset)
        and adjusts the delay dynamically to avoid hitting rate limits.

        Common headers:
        - X-RateLimit-Remaining: Number of requests remaining in current window
        - X-RateLimit-Reset: Unix timestamp when the rate limit resets
        - X-RateLimit-Limit: Total number of requests allowed in window

        Args:
            headers: Response headers from API as a dictionary.

        Returns:
            None: Updates internal state based on header information.
        """
        if not self.respect_headers:
            return

        # Normalize header keys to lowercase for case-insensitive lookup
        normalized_headers = {k.lower(): v for k, v in headers.items()}

        # Check for X-RateLimit-Remaining header
        remaining_str = normalized_headers.get("x-ratelimit-remaining")
        reset_str = normalized_headers.get("x-ratelimit-reset")
        limit_str = normalized_headers.get("x-ratelimit-limit")

        if remaining_str is not None:
            try:
                remaining = int(remaining_str)

                # If we're running low on requests, increase delay
                if remaining < 10:
                    self.console.print(
                        f"[yellow]Rate limit warning: only {remaining} requests remaining[/yellow]"
                    )
                    # Increase delay significantly when running low
                    self._dynamic_delay = self.delay_seconds * 2.0
                elif remaining < 50:
                    # Moderate increase when getting lower
                    self._dynamic_delay = self.delay_seconds * 1.5
                else:
                    # Reset to normal delay when plenty of quota available
                    self._dynamic_delay = None

            except ValueError:
                # Invalid remaining count, ignore
                pass

        # Check for reset timestamp
        if reset_str is not None and remaining_str is not None:
            try:
                remaining = int(remaining_str)
                reset_timestamp = int(reset_str)
                current_timestamp = int(datetime.now(timezone.utc).timestamp())

                # If we're out of requests, calculate wait time until reset
                if remaining == 0:
                    time_until_reset = reset_timestamp - current_timestamp
                    if time_until_reset > 0:
                        self.console.print(
                            f"[bold red]Rate limit exceeded! Waiting {time_until_reset}s until reset[/bold red]"
                        )
                        time.sleep(time_until_reset + 1)  # Add 1 second buffer
                        self._dynamic_delay = None  # Reset dynamic delay after waiting

            except ValueError:
                # Invalid timestamp, ignore
                pass

        # Optionally log rate limit info for debugging
        if limit_str is not None and remaining_str is not None:
            try:
                limit = int(limit_str)
                remaining = int(remaining_str)
                used = limit - remaining
                self.console.print(
                    f"[dim]API rate limit: {used}/{limit} requests used[/dim]"
                )
            except ValueError:
                pass
