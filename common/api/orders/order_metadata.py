from common.api.request import Request
from common.order.order_type import OrderType

class OrderMetadata(Request):
    def __init__(self, order_type: OrderType, account_id: str, client_order_id: str = None):
        self.order_type: OrderType = order_type
        self.account_id: str = account_id
        self.client_order_id = client_order_id