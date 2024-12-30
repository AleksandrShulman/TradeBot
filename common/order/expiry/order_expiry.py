from abc import ABC
from datetime import datetime


class OrderExpiry(ABC):
    def __init__(self, expiry_date: datetime.date, all_or_none=False):
        self.expiry_date: datetime.date = expiry_date
        self.all_or_none: bool = all_or_none
        self.label: str = self.get_label()

    # TODO: Find an elegant way to apply this
    def get_label(self):
        return None

    def valid_at(self, trade_date: datetime.date) -> bool:
        return trade_date < self.expiry_date

    def __str__(self):
        return f"Expiry date: {self.expiry_date} | All or None: {self.all_or_none}"

    def __repr__(self):
        return f"OrderExpiry({self.expiry_date}, {self.all_or_none})"