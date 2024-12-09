from enum import Enum


class OrderPriceType(Enum):
    MARKET = 0,
    EVEN = 1,
    NET_CREDIT = 2,
    NET_DEBIT = 3
    LIMIT = 4
