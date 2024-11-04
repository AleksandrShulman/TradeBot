from common.order.expiry.order_expiry import OrderExpiry
from common.order.order_line import OrderLine
from common.order.order_price import OrderPrice


class Order:
    def __init__(self, order_lines: list[OrderLine], order_price: OrderPrice, expiry: OrderExpiry):
        self.order_lines = order_lines
        self.order_price = order_price
        self.expiry = expiry

