from enum import Enum


class OrderStatus(Enum):
    OPEN = 0,
    EXECUTED = 1,
    CANCELLED = 2,
    INDIVIDUAL_FILLS = 3,
    CANCEL_REQUESTED = 4,
    EXPIRED = 5,
    REJECTED = 6