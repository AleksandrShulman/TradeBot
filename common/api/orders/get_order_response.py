from common.api.response import Response
from common.order.placed_order import PlacedOrder


class GetOrderResponse(Response):
    def __init__(self, order: PlacedOrder):
        self.placed_order = order

    def __str__(self):
        return f"Order: {self.placed_order}"
