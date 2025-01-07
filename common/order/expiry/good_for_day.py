import datetime

from common.order.expiry.order_expiry import OrderExpiry


class GoodForDay(OrderExpiry):
    def __init__(self):
        super().__init__(datetime.datetime.today().date())

    def __str__(self):
        return f"Good for Day: {self.expiry_date}"
