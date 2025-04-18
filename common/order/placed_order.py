from pydantic import BaseModel

from common.order.order import Order
from common.order.placed_order_details import PlacedOrderDetails


class PlacedOrder(BaseModel):
    order: Order
    placed_order_details: PlacedOrderDetails

    def get_order(self):
        return self.order

    def to_dict(self):
        return {
            "order" : self.order,
            "placed_order_details": self.placed_order_details
    }