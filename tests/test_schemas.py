from datetime import date

import pytest
from pydantic import ValidationError

from receipt_rag.schemas import LineItem, Receipt


def _error_locs(exc: ValidationError) -> list[tuple[str | int, ...]]:
    return [tuple(error["loc"]) for error in exc.errors()]


def test_receipt_schema():
    receipt = Receipt(
        merchant="Test Merchant",
        date=date(2021, 1, 1),
        currency="USD",
        total=100.00,
        items=[
            {
                "quantity": 1.0,
                "unit_price": 100.00,
                "description": "Test Item",
                "discount": 0.00,
                "tax": 0.00,
            },
        ],
    )

    assert receipt.model_dump() == {
        "merchant": "Test Merchant",
        "date": date(2021, 1, 1),
        "currency": "USD",
        "total": 100.00,
        "items": [
            {
                "quantity": 1.0,
                "unit_price": 100.00,
                "description": "Test Item",
                "discount": 0.00,
                "tax": 0.00,
            }
        ],
    }
    assert receipt.model_dump(mode="json") == {
        "merchant": "Test Merchant",
        "date": "2021-01-01",
        "currency": "USD",
        "total": 100.00,
        "items": [
            {
                "quantity": 1.0,
                "unit_price": 100.00,
                "description": "Test Item",
                "discount": 0.00,
                "tax": 0.00,
            }
        ],
    }


def test_line_item_rejects_non_numeric_unit_price():
    with pytest.raises(ValidationError) as exc_info:
        LineItem(
            quantity=1.0,
            unit_price="ten",
            description="Test Item",
        )

    assert ("unit_price",) in _error_locs(exc_info.value)


def test_receipt_rejects_malformed_date():
    with pytest.raises(ValidationError) as exc_info:
        Receipt(
            merchant="Test Merchant",
            date="31/13/2021",
            currency="USD",
            total=100.00,
            items=[],
        )

    assert ("date",) in _error_locs(exc_info.value)


def test_receipt_rejects_invalid_nested_line_item():
    with pytest.raises(ValidationError) as exc_info:
        Receipt(
            merchant="Test Merchant",
            date=date(2021, 1, 1),
            currency="USD",
            total=100.00,
            items=[
                {
                    "quantity": 1.0,
                    "unit_price": "not-a-price",
                    "description": "Test Item",
                }
            ],
        )

    assert ("items", 0, "unit_price") in _error_locs(exc_info.value)


def _receipt_kwargs(**overrides) -> dict:
    valid = {
        "merchant": "Test Merchant",
        "date": date(2021, 1, 1),
        "currency": "CZK",
        "total": 100.00,
        "items": [{"quantity": 1.0, "unit_price": 100.00, "description": "Test Item"}],
    }
    return valid | overrides


def test_line_item_discount_and_tax_are_optional():
    item = LineItem(quantity=1.0, unit_price=5.0, description="Rohlik")

    assert item.discount is None
    assert item.tax is None


@pytest.mark.parametrize("quantity", [0, -1])
def test_line_item_rejects_zero_or_negative_quantity(quantity):
    with pytest.raises(ValidationError) as exc_info:
        LineItem(quantity=quantity, unit_price=5.0, description="Rohlik")

    assert ("quantity",) in _error_locs(exc_info.value)


def test_line_item_rejects_empty_description():
    with pytest.raises(ValidationError) as exc_info:
        LineItem(quantity=1.0, unit_price=5.0, description="")

    assert ("description",) in _error_locs(exc_info.value)


def test_receipt_rejects_negative_total():
    with pytest.raises(ValidationError) as exc_info:
        Receipt(**_receipt_kwargs(total=-1.0))

    assert ("total",) in _error_locs(exc_info.value)


def test_receipt_rejects_empty_items():
    with pytest.raises(ValidationError) as exc_info:
        Receipt(**_receipt_kwargs(items=[]))

    assert ("items",) in _error_locs(exc_info.value)


@pytest.mark.parametrize("currency", ["", "czk", "CZ", "Czech crowns"])
def test_receipt_rejects_non_iso_currency(currency):
    with pytest.raises(ValidationError) as exc_info:
        Receipt(**_receipt_kwargs(currency=currency))

    assert ("currency",) in _error_locs(exc_info.value)
