from common.api.orders.order_metadata import OrderMetadata
from common.api.orders.order_preview import OrderPreview
from common.api.orders.preview_order_response import PreviewOrderResponse


class PreviewModifyOrderResponse(PreviewOrderResponse):
    def __init__(self, order_metadata: OrderMetadata, preview_id, order_id, order_preview: OrderPreview):
        super().__init__(order_metadata, preview_id, order_preview)
        self.order_id = order_id
