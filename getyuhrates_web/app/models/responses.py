"""Response models for the GetYuhRates web application."""

from typing import Any
from pydantic import BaseModel, Field


class MessageResponse(BaseModel):
    """Generic message response.

    Attributes:
        message (str): Response message.
        success (bool): Whether the operation was successful.
    """

    message: str = Field(..., description="Response message")
    success: bool = Field(default=True, description="Success status")


class CurrencyRateResponse(BaseModel):
    """Response model for currency rate data.

    Attributes:
        success (bool): Whether the request was successful.
        source (str): Source currency code.
        currencies (list[str]): Target currency codes.
        rates (dict[str, float]): Exchange rates mapping.
        reason (str | None): Error reason if unsuccessful.
        file_location (str | None): Path to saved file if applicable.
    """

    success: bool = Field(..., description="Request success status")
    source: str = Field(..., description="Source currency")
    currencies: list[str] = Field(..., description="Target currencies")
    rates: dict[str, float] = Field(default_factory=dict, description="Exchange rates")
    reason: str | None = Field(default=None, description="Error reason")
    file_location: str | None = Field(default=None, description="Saved file path")


class ReportInfo(BaseModel):
    """Information about a report file.

    Attributes:
        filename (str): Name of the file.
        size (int): File size in bytes.
        modified (str): Last modified timestamp.
        path (str): Full path to the file.
    """

    filename: str = Field(..., description="File name")
    size: int = Field(..., description="File size in bytes")
    modified: str = Field(..., description="Last modified timestamp")
    path: str = Field(..., description="Full file path")


class ConfigResponse(BaseModel):
    """Response model for configuration data.

    Attributes:
        source (list[str]): Source currencies.
        currencies (list[str]): Target currencies.
        always_download (str): Always download setting.
        output_folder (str): Output folder path (read-only).
        output_format (str): Output format.
        send_emails (bool): Send emails flag.
        sender_email (str): Sender email address.
        recipients (list[str]): Recipient email addresses.
        subject_title (str): Email subject.
        email_body (str): Email body.
    """

    source: list[str] = Field(..., description="Source currencies")
    currencies: list[str] = Field(..., description="Target currencies")
    always_download: str = Field(..., description="Always download (Y/N)")
    output_folder: str = Field(..., description="Output folder (read-only)")
    output_format: str = Field(..., description="Output format")
    send_emails: bool = Field(..., description="Send emails flag")
    sender_email: str = Field(..., description="Sender email")
    recipients: list[str] = Field(..., description="Recipient emails")
    subject_title: str = Field(..., description="Email subject")
    email_body: str = Field(..., description="Email body")
