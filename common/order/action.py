from enum import Enum


class Action(Enum):
    BUY_TO_OPEN = 0,
    SELL_TO_OPEN = 1,
    BUY_TO_CLOSE = 2,
    SELL_TO_CLOSE = 3
