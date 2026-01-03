"""Tests for CurrencyResult TypedDict.

This module contains tests to verify the CurrencyResult structure and usage.
"""

from getyuhrates.currencyresult import CurrencyResult


def test_currency_result_structure() -> None:
    """Test that CurrencyResult can be created with all required fields.

    This test verifies the structure of a successful CurrencyResult.
    """
    result: CurrencyResult = {
        "success": True,
        "source": "USD",
        "currencies": ["EUR", "GBP"],
        "rates": {"USDEUR": 0.85, "USDGBP": 0.74},
        "reason": None,
        "file_location": None,
    }

    assert result["success"] is True
    assert result["source"] == "USD"
    assert result["currencies"] == ["EUR", "GBP"]
    assert result["rates"]["USDEUR"] == 0.85
    assert result["rates"]["USDGBP"] == 0.74
    assert result["reason"] is None
    assert result["file_location"] is None


def test_currency_result_failure() -> None:
    """Test that CurrencyResult can represent a failed request.

    This test verifies the structure of a failed CurrencyResult.
    """
    result: CurrencyResult = {
        "success": False,
        "source": "USD",
        "currencies": ["EUR"],
        "rates": {},
        "reason": "Invalid API key",
        "file_location": None,
    }

    assert result["success"] is False
    assert result["reason"] == "Invalid API key"
    assert len(result["rates"]) == 0


def test_currency_result_with_file() -> None:
    """Test that CurrencyResult can include a file location.

    This test verifies that file_location field works correctly.
    """
    result: CurrencyResult = {
        "success": True,
        "source": "GBP",
        "currencies": ["BBD"],
        "rates": {"GBPBBD": 2.5},
        "reason": None,
        "file_location": "/tmp/output/rates.csv",
    }

    assert result["file_location"] == "/tmp/output/rates.csv"
    assert result["source"] == "GBP"
