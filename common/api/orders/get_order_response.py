from pydantic import BaseModel

from common.api.response import Response
from common.order.placed_order import PlacedOrder


class GetOrderResponse(BaseModel, Response):
    placed_order: PlacedOrder

    def __str__(self):
        return f"Order: {self.placed_order}"
