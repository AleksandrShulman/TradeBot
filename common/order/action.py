from enum import Enum


class Action(Enum):
    BUY_OPEN = 0,
    SELL_OPEN = 1,
    BUY_CLOSE = 2,
    SELL_CLOSE = 3,
    BUY = 4,
    SELL = 5
