
from common.order.order import Order
from common.order.placed_order_details import PlacedOrderDetails


class PlacedOrder:
    def __init__(self, order: Order, placed_order_details: PlacedOrderDetails):
        self.order = order
        self.placed_order_details = placed_order_details

    def get_order(self):
        return self.order