from common.api.orders.order_metadata import OrderMetadata
from common.api.request import Request
from common.order.order import Order

class PlaceOrderRequest(Request):
    def __init__(self, order_metadata: OrderMetadata, preview_id: str, order: Order):
        self.order_metadata: OrderMetadata = order_metadata
        self.preview_id: str = preview_id
        self.order: Order = order
