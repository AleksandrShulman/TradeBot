from common.api.orders.order_metadata import OrderMetadata
from common.api.orders.order_placement_message import OrderPlacementMessage
from common.api.orders.order_preview import OrderPreview
from common.api.request_status import RequestStatus
from common.api.response import Response

class PreviewOrderResponse(Response):
    def __init__(self, order_metadata: OrderMetadata, preview_id: str, order_preview: OrderPreview, request_status: RequestStatus = RequestStatus.SUCCESS, order_message: OrderPlacementMessage=None):
        self.order_metadata: OrderMetadata = order_metadata
        self.preview_id: str = preview_id
        self.preview_order_info: OrderPreview = order_preview
        self.request_status: RequestStatus = request_status
        self.order_message: OrderPlacementMessage = order_message
