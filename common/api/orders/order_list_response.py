from common.api.response import Response
from common.order.placed_order import PlacedOrder


class ListOrdersResponse(Response):
    def __init__(self, order_list: list[PlacedOrder]):
        self.order_list: list[PlacedOrder] = order_list

    def get_order_list(self):
        return self.order_list

    def __str__(self):
        return f"Order List: {str(self.order_list)}"

    def __repr__(self):
        return self.__str__()