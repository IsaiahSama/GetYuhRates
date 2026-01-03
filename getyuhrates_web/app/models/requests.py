"""Request models for the GetYuhRates web application."""

from pydantic import BaseModel, Field


class CurrencyRateRequest(BaseModel):
    """Request model for currency rate retrieval.

    Attributes:
        source (list[str]): List of source currency codes (e.g., ["USD", "GBP"]).
        currencies (list[str]): List of target currency codes to convert to.
        save_to_file (bool): Whether to save the results to a CSV file.
    """

    source: list[str] = Field(
        ...,
        min_length=1,
        description="Source currency codes"
    )
    currencies: list[str] = Field(
        ...,
        min_length=1,
        description="Target currency codes"
    )
    save_to_file: bool = Field(
        default=False,
        description="Whether to save results to CSV"
    )


class ConfigUpdateRequest(BaseModel):
    """Request model for configuration updates.

    Attributes:
        source (list[str]): Default source currencies.
        currencies (list[str]): Default target currencies.
        always_download (str): Whether to always download files (Y/N).
        output_format (str): Output format (CSV or PDF).
        send_emails (bool): Whether to send email notifications.
        sender_email (str): Email address for sending notifications.
        recipients (list[str]): List of recipient email addresses.
        subject_title (str): Email subject line.
        email_body (str): Email body content.
    """

    source: list[str] = Field(
        ...,
        min_length=1,
        description="Default source currencies"
    )
    currencies: list[str] = Field(
        ...,
        min_length=1,
        description="Default target currencies"
    )
    always_download: str = Field(
        ...,
        pattern="^[YN]$",
        description="Always download files (Y or N)"
    )
    output_format: str = Field(
        ...,
        pattern="^(CSV|PDF)$",
        description="Output format (CSV or PDF)"
    )
    send_emails: bool = Field(
        default=False,
        description="Send email notifications"
    )
    sender_email: str = Field(
        ...,
        description="Sender email address"
    )
    recipients: list[str] = Field(
        default_factory=list,
        description="Recipient email addresses"
    )
    subject_title: str = Field(
        ...,
        description="Email subject line"
    )
    email_body: str = Field(
        ...,
        description="Email body content"
    )
