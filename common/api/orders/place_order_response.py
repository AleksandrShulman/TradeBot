from common.api.orders.order_metadata import OrderMetadata
from common.api.orders.order_placement_message import OrderPlacementMessage
from common.api.response import Response
from common.order.order import Order
from common.order.placed_order import PlacedOrder


class PlaceOrderResponse(Response):
    def __init__(self, order_metadata: OrderMetadata, preview_id: str,
                 order_id:str, order: Order, order_placement_messages: list[OrderPlacementMessage]):
        self.order_metadata: OrderMetadata = order_metadata
        self.preview_id: str = preview_id
        self.order_id: str = order_id
        self.order: Order = order
        self.order_placement_messages: list[OrderPlacementMessage] = order_placement_messages
