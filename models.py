""" Модели для API запросов и ответов
"""
from typing import List

from pydantic import (
    BaseModel,
    conint,
    confloat
)

from constants import *

__all__ = (
    'TotalPriceRequest',
    'TotalPriceResponse',
    'USCode',
    'USCodeResponse',
)

# note: правильнее использовать Decimal для расчетов
# вместо float (сильная погрешность при расчетах)


class TotalPriceRequest(BaseModel):
    """
    """
    qty: conint(gt=0)
    price: confloat(ge=0)
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
    def us_tax(self):
        return self.us_code.tax

    @property
    def total_price(self):
        return self.gross_total_price * \
               self.discount_for_total_price / 100 * \
               (100 - self.us_tax) / 100


class TotalPriceResponse(BaseModel):
    discount_for_total_price: float
    us_tax: float
    total_price: float


class USCode(BaseModel):
    us_code: str
    us_tax: float


class USCodeResponse(BaseModel):
    __root__: List[USCode]
