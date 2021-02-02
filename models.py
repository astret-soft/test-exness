from decimal import Decimal
from typing import List

from cached_property import cached_property
from pydantic import (
    BaseModel,
    conint,
    condecimal,
)

from constants import *

__all__ = (
    'TotalPriceRequest',
    'TotalPriceResponse',
    'USCode',
    'USCodeResponse',
)


class TotalPriceRequest(BaseModel):
    qty: conint(gt=0)
    price: condecimal(ge=Decimal(0))
    us_code: USCodeEnum

    @cached_property
    def gross_total_price(self) -> Decimal:
        return self.qty * self.price

    @cached_property
    def discount_for_total_price(self) -> Decimal:
        return next(
            discount for edge, discount
            in reversed(TOTAL_COST_TO_DISCOUNT)
            if self.gross_total_price >= edge
        )

    @cached_property
    def us_tax(self) -> Decimal:
        return self.us_code.value[1]

    @cached_property
    def total_price(self) -> Decimal:
        return self.gross_total_price * \
               self.discount_for_total_price * \
               (1 - self.us_tax)


class TotalPriceResponse(BaseModel):
    discount_for_total_price: Decimal
    us_tax: Decimal
    total_price: Decimal


class USCode(BaseModel):
    us_code: str
    us_tax: Decimal


class USCodeResponse(BaseModel):
    __root__ = List[USCode]
