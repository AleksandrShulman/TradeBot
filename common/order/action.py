from enum import Enum


class Action(Enum):
    BUY_OPEN = 0,
    SELL_OPEN = 1,
    BUY_CLOSE = 2,
    SELL_CLOSE = 3,
    BUY = 4,
    SELL = 5

    @staticmethod
    def is_long(action):
        return action in LONGS

    @staticmethod
    def is_short(action):
        return not Action.is_long(action)


SHORTS = {Action.SELL, Action.SELL_OPEN, Action.SELL_CLOSE}
LONGS = {Action.BUY, Action.BUY_OPEN, Action.BUY_CLOSE}