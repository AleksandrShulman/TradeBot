from common.api.orders.OrderCancellationMessage import OrderCancellationMessage
from common.api.request import Request

class OrderModification:
    def __init__(self, order_id, preview_id):
        self.order_id = order_id
        self.preview_id = preview_id

class ModifyOrderResponse(Request):
    def __init__(self, order_modifications: list[OrderModification]):
        self.order_modifications: list[OrderModification] = order_modifications