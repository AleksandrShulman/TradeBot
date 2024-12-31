from common.api.request import Request
from common.order.order import Order
from common.order.order_type import OrderType


class CancelOrderRequest(Request):
    def __init__(self, account_id: str, order_id: str):
        self.account_id = account_id
        self.order_id = order_id
