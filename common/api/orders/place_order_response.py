from common.api.orders.order_metadata import OrderMetadata
from common.api.orders.order_placement_message import OrderPlacementMessage
from common.api.response import Response
from common.order.order import Order


class PlaceOrderResponse(Response):
    order_metadata: OrderMetadata
    preview_id: str
    order_id: str
    order: Order
    order_placement_messages: list[OrderPlacementMessage] = []