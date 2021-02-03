""" Справочники
"""
from enum import Enum

__all__ = (
    'TOTAL_COST_TO_DISCOUNT',
    'USCodeEnum',
    'USCodeTaxes',
)

# note: правильнее использовать Decimal для расчетов
# вместо float (сильная погрешность при расчетах)
# нет требования в задании использовать БД (с учетом < 100 штатов нет смысла использовать БД)

TOTAL_COST_TO_DISCOUNT = (
    (1000, 3.),
    (5000, 5.),
    (7000, 7.),
    (10000, 10.),
    (50000, 15.),
)


class USCodeEnum(Enum):
    UT = 'UT'
    NV = 'NV'
    TX = 'TX'
    AL = 'AL'
    CA = 'CA'

    @property
    def tax(self) -> float:
        return USCodeTaxes[self]


USCodeTaxes = {
    USCodeEnum.UT: 6.85,
    USCodeEnum.NV: 8.,
    USCodeEnum.TX: 6.25,
    USCodeEnum.AL: 4.,
    USCodeEnum.CA: 8.25,
}
