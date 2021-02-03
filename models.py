from typing import List
from decimal import Decimal

from pydantic import (
    BaseModel,
    conint,
    condecimal
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

    @property
    def gross_total_price(self):
        return self.qty * self.price

    @property
    def discount_for_total_price(self):
        return next(
            discount for edge, discount
            in reversed(TOTAL_COST_TO_DISCOUNT)
            if self.gross_total_price >= edge
        )

    @property
    def us_tax(self) :
        return self.us_code.value[1]

    @property
    def total_price(self):
        return self.gross_total_price * \
               self.discount_for_total_price * \
               (1 - self.us_tax)


class TotalPriceResponse(BaseModel):
    discount_for_total_price: float
    us_tax: float
    total_price: float


class USCode(BaseModel):
    us_code: str
    us_tax: float


class USCodeResponse(BaseModel):
    __root__: List[USCode]

