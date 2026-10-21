from datetime import date

from pydantic import BaseModel, Field


class LineItem(BaseModel):
    quantity: float = Field(gt=0)
    unit_price: float = Field(ge=0)
    description: str = Field(min_length=1)
    discount: float | None = None
    tax: float | None = None


class Receipt(BaseModel):
    merchant: str
    date: date
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    total: float = Field(ge=0)
    items: list[LineItem] = Field(min_length=1)
