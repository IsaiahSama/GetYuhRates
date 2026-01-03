"""Routes for the home page."""

from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .reports import get_report_files

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request) -> Any:
    """Render the home page with recent reports.

    Args:
        request (Request): The HTTP request object.

    Returns:
        Any: Rendered HTML template.
    """
    # Get recent reports (limit to 5)
    all_reports = get_report_files()
    recent_reports = all_reports[:5] if len(all_reports) > 5 else all_reports

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "recent_reports": recent_reports,
        }
    )
