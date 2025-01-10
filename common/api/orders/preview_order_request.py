from common.api.orders.order_metadata import OrderMetadata
from common.api.request import Request
from common.order.order import Order

class PreviewOrderRequest(Request):
    def __init__(self, order_metadata: OrderMetadata, order: Order):
        self.order_metadata: OrderMetadata = order_metadata
        self.order = order
