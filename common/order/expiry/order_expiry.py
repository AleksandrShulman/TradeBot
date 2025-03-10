from abc import ABC
from datetime import datetime

from common.test.util.test_object_util import expiry


class OrderExpiry(ABC):
    def __init__(self, expiry_date: datetime.date, all_or_none=False):
        self.expiry_date: datetime.date = expiry_date
        self.all_or_none: bool = all_or_none

    def valid_at(self, trade_date: datetime.date) -> bool:
        return trade_date < self.expiry_date

    def __str__(self):
        return f"Expiry date: {self.expiry_date} | All or None: {self.all_or_none}"

    def __repr__(self):
        return f"OrderExpiry({self.expiry_date}, {self.all_or_none})"

    def __eq__(self, other):
        if self.all_or_none != other.all_or_none:
            return False
        if self.expiry_date != other.expiry_date:
            return False

        return True