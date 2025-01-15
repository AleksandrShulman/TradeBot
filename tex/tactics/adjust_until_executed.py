from common.order.order import Order
from common.order.order_price import OrderPrice
from common.order.order_price_type import OrderPriceType


class AdjustUntilExecuted():
    def __init__(self, order: Order, reserve_price: OrderPrice):
        order_price: OrderPrice = order.order_price
        if order_price.order_price_type == OrderPriceType.NET_CREDIT:
            if reserve_price.order_price_type == OrderPriceType.NET_CREDIT and other.:
                if reserve_price. >
        pass