from decimal import Decimal
from enum import Enum

__all__ = (
    'TOTAL_COST_TO_DISCOUNT',
    'USCodeEnum',
)

TOTAL_COST_TO_DISCOUNT = (
    (Decimal(1000), Decimal(0.03)),
    (Decimal(5000), Decimal(0.05)),
    (Decimal(7000), Decimal(0.07)),
    (Decimal(10000), Decimal(0.1)),
    (Decimal(50000), Decimal(0.15)),
)


class USCodeEnum(Enum):
    UT = ('UT', Decimal(6.85))
    NV = ('NV', Decimal(8.))
    TX = ('TX', Decimal(6.25))
    AL = ('AL', Decimal(4.))
    CA = ('CA', Decimal(8.25))
