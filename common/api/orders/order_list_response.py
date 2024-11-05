from common.api.response import Response
from common.order.order import Order


class OrderListResponse(Response):
    def __init__(self, order_list: list[Order]):
        self.order_list = order_list

    def get_order_list(self):
        return self.order_list

    def __str__(self):
        return f"Account List: {str(self.order_list)}"

    def __repr__(self):
        return self.__str__()