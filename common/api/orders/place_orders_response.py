from common.api.orders.OrderPlacementMessage import OrderPlacementMessage
from common.api.response import Response
from common.order.order import Order

class PlaceOrdersResponse(Response):
    def __init__(self, order_ids: list[str],orders: list[Order], messages: list[OrderPlacementMessage]):
        self.order_ids: list[str] = order_ids
        self.orders: list[Order] = orders
        self.messages: list[OrderPlacementMessage] = messages

    def __str__(self):
        return f"Order_ids: {self.order_ids}"