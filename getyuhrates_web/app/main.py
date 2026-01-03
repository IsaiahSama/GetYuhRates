"""FastAPI application definition for GetYuhRates web service."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import load_env
from .routes import home, rates, reports, config


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan manager.

    Handles startup and shutdown events.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: Control back to the application.
    """
    # Startup: Load environment variables
    load_env()

    yield

    # Shutdown: Clean up resources if needed
    pass


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance.
    """
    app = FastAPI(
        title="GetYuhRates Web Service",
        description="Web interface for currency exchange rate management",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Include routers
    app.include_router(home.router, tags=["Home"])
    app.include_router(rates.router, tags=["Rates"])
    app.include_router(reports.router, tags=["Reports"])
    app.include_router(config.router, tags=["Configuration"])

    return app


# Create the application instance
app = create_app()
