from typing import Optional

from common.api.request import Request
from common.order.order_type import OrderType

class OrderMetadata(Request):
    order_type: OrderType
    account_id: str
    client_order_id: Optional[str] = None
