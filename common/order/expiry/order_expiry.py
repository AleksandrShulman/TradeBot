from abc import ABC
from datetime import datetime


class OrderExpiry(ABC):
    def __init__(self, expiry_date: datetime, all_or_none=False):
        self.expiry_date: datetime = expiry_date
        self.all_or_none = all_or_none

    def valid_at(self, trade_date) -> bool:
        return trade_date < self.expiry_date
