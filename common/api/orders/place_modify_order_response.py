from common.api.orders.order_metadata import OrderMetadata
from common.api.orders.order_placement_message import OrderPlacementMessage
from common.api.orders.place_order_response import PlaceOrderResponse
from common.api.response import Response
from common.order.order import Order
from common.order.placed_order import PlacedOrder


class PlaceModifyOrderResponse(PlaceOrderResponse):
    def __init__(self, order_metadata: OrderMetadata, preview_id: str, previous_order_id: str, order_id: str, order: Order,
                 order_placement_messages: list[OrderPlacementMessage]):
        super().__init__(order_metadata, preview_id, order_id, order, order_placement_messages)
        self.previous_order_id = previous_order_id
