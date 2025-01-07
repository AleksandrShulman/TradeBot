from common.finance.amount import Amount
from common.order.order_price_type import OrderPriceType


class OrderPrice:
    def __init__(self, order_price_type: OrderPriceType, price: Amount):
        self.order_price_type: OrderPriceType = order_price_type

        if order_price_type is OrderPriceType.NET_EVEN and price != Amount(0,0):
            raise Exception("Cannot have a price when it is supposed to be EVEN")

        self.price: Amount = price

    def __str__(self):
        return f"{self.order_price_type.name}: {self.price}"

    def __eq__(self, other):
        if self.order_price_type != other.order_price_type:
            return False
        if self.price != other.price:
            return False

        return True