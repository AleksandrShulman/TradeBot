from common.api.request import Request
from common.order.order import Order
from common.order.order_type import OrderType

class PlaceOrdersRequest(Request):
    def __init__(self, account_id: str, order_type: OrderType, orders: list[Order], preview_ids: list[str]):
        self.order_type = order_type
        self.account_id = account_id
        self.orders = orders
        self.preview_ids = preview_ids
