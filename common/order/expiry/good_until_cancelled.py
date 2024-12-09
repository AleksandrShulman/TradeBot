from common.order.expiry.order_expiry import OrderExpiry


class GoodUntilCancelled(OrderExpiry):
    def __init__(self, all_or_none: bool):
        super().__init__(None, True)

    def __str__(self):
        return f"Good for until cancelled. All-or-none: {self.all_or_none}"
