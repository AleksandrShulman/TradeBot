
from common.api.response import Response
from common.order.order import Order


class PlaceOrderResponse(Response):
    def __init__(self, order: Order):
        self.order = order

    def __str__(self):
        return f"Order: {self.order}"