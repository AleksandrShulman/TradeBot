import datetime

from common.api.request import Request
from common.order.order import Order
from common.order.order_type import OrderType

class PreviewOrdersRequest(Request):
    def __init__(self, order_type: OrderType, account_id: str, orders: list[Order]):
        self.order_type: OrderType = order_type
        self.account_id: str = account_id
        self.orders: list[Order] = orders