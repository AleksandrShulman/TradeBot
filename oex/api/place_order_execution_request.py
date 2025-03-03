from common.api.request import Request
from common.order.order import Order


class PlaceOrderExecutionRequest(Request):
    def __init__(self, order: Order):
        self.order = order


