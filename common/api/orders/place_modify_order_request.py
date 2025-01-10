from common.api.orders.order_metadata import OrderMetadata
from common.api.orders.place_order_request import PlaceOrderRequest
from common.order.order import Order


class PlaceModifyOrderRequest(PlaceOrderRequest):
    def __init__(self, order_metadata: OrderMetadata, preview_id: str, order_id_to_modify: str, order: Order):
        super().__init__(order_metadata, preview_id, order)
        self.order_id_to_modify: str = order_id_to_modify