from common.api.orders.preview_orders_request import PreviewOrdersRequest
from common.api.request import Request
from common.order.order import Order
from common.order.order_type import OrderType


class ModifyOrderRequest(Request):
    def __init__(self, order_id: str, preview_orders_request: PreviewOrdersRequest):
        self.order_id: str = order_id
        self.preview_orders_request: PreviewOrdersRequest = preview_orders_request
