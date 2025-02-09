from urllib3 import request

from common.api.orders.order_metadata import OrderMetadata
from common.api.orders.order_preview import OrderPreview
from common.api.orders.preview_order_response import PreviewOrderResponse
from common.api.request_status import RequestStatus


class PreviewModifyOrderResponse(PreviewOrderResponse):
    def __init__(self, order_metadata: OrderMetadata, preview_id, order_id, order_preview: OrderPreview, request_status:RequestStatus = RequestStatus.SUCCESS):
        super().__init__(order_metadata, preview_id, order_preview, request_status=request_status)
        self.order_id = order_id
