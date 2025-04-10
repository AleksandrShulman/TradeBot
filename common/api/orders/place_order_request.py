from common.api.orders.order_metadata import OrderMetadata
from common.api.request import Request
from common.order.order import Order

class PlaceOrderRequest(Request):
    order_metadata: OrderMetadata
    preview_id: str
    order: Order
