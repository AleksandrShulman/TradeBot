from enum import Enum


class OrderPriceType(Enum):
    MARKET = 0
    NET_EVEN = 1
    NET_CREDIT = 2
    NET_DEBIT = 3
    LIMIT = 4
    STOP_LIMIT = 5
    TRAILING_STOP_CNST_BY_LOWER_TRIGGER = 6
    MARKET_ON_CLOSE = 7
    LIMIT_ON_OPEN = 8
    LIMIT_ON_CLOSE = 9
    TRAILING_STOP_PRCT = 10
    UPPER_TRIGGER_BY_HIDDEN_STOP = 11

    def __str__(self):
        return self.name  # Ensures string conversion returns the name