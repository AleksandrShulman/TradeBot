from typing import Optional

from common.api.orders.order_metadata import OrderMetadata
from common.api.orders.order_placement_message import OrderPlacementMessage
from common.api.orders.order_preview import OrderPreview
from common.api.request_status import RequestStatus
from common.api.response import Response

class PreviewOrderResponse(Response):
    order_metadata: OrderMetadata
    preview_id: str
    preview_order_info: OrderPreview
    request_status: RequestStatus = RequestStatus.SUCCESS
    order_message: Optional[OrderPlacementMessage] = None
