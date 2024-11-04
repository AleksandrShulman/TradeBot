from enum import Enum


class OrderPriceType(Enum):
    MARKET = 0,
    EVEN = 1,
    LIMIT_CREDIT = 2,
    LIMIT_DEBIT = 3
