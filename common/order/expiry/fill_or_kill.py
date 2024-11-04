import datetime

from common.order.expiry.order_expiry import OrderExpiry


class FillOrKill(OrderExpiry):

    def __init__(self):
        five_seconds_from_now = datetime.datetime.now() + datetime.timedelta(seconds=5)
        super().__init__(five_seconds_from_now, True)

    def __str__(self):
        return f"Fill or Kill: {self.expiry_date}"
