"""Routes for report management."""

import os
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

from ..models.responses import MessageResponse, ReportInfo
from ..config import get_reports_dir

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def get_report_files() -> list[dict[str, Any]]:
    """Get list of all report files with metadata.

    Returns:
        list[dict[str, Any]]: List of report information dictionaries.
    """
    reports_dir = get_reports_dir()
    reports = []

    if not reports_dir.exists():
        return reports

    for file_path in reports_dir.iterdir():
        if file_path.is_file():
            stat = file_path.stat()
            modified_time = datetime.fromtimestamp(stat.st_mtime)

            reports.append({
                "filename": file_path.name,
                "size": stat.st_size,
                "modified": modified_time.strftime("%Y-%m-%d %H:%M:%S"),
                "path": str(file_path),
            })

    # Sort by modified time, newest first
    reports.sort(key=lambda x: x["modified"], reverse=True)

    return reports


@router.get("/reports", response_class=HTMLResponse)
async def reports_page(request: Request) -> Any:
    """Render the reports management page.

    Args:
        request (Request): The HTTP request object.

    Returns:
        Any: Rendered HTML template.
    """
    reports = get_report_files()

    return templates.TemplateResponse(
        "reports.html",
        {
            "request": request,
            "reports": reports,
        }
    )


@router.get("/reports/download/{filename}")
async def download_report(filename: str) -> FileResponse:
    """Download a specific report file.

    Args:
        filename (str): Name of the file to download.

    Returns:
        FileResponse: The file to download.

    Raises:
        HTTPException: If file not found or invalid filename.
    """
    # Security check: prevent directory traversal
    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    reports_dir = get_reports_dir()
    file_path = reports_dir / filename

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Report not found")

    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type="application/octet-stream"
    )


@router.delete("/reports/delete/{filename}", response_model=MessageResponse)
async def delete_report(filename: str) -> dict[str, Any]:
    """Delete a specific report file.

    Args:
        filename (str): Name of the file to delete.

    Returns:
        dict[str, Any]: Success message.

    Raises:
        HTTPException: If file not found or invalid filename.
    """
    # Security check: prevent directory traversal
    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    reports_dir = get_reports_dir()
    file_path = reports_dir / filename

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Report not found")

    try:
        file_path.unlink()
        return {
            "message": f"Report '{filename}' deleted successfully",
            "success": True
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting report: {str(e)}"
        )


@router.get("/reports/list", response_model=list[ReportInfo])
async def list_reports() -> list[dict[str, Any]]:
    """Get list of all reports as JSON.

    Returns:
        list[dict[str, Any]]: List of report information.
    """
    return get_report_files()
