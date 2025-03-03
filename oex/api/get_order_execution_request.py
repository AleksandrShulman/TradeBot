from common.api.request import Request
from common.order.order import Order


class GetOrderExecutionRequest(Request):
    def __init__(self, managed_order_id: str):
        self.managed_order_id: str = managed_order_id


