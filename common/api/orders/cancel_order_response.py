from common.api.orders.order_cancellation_message import OrderCancellationMessage
from common.api.request import Request


class CancelOrderResponse(Request):
    def __init__(self, order_id: str, cancel_time: str, messages: list[OrderCancellationMessage]):
        self.order_id = order_id
        self.cancel_time = cancel_time
        self.messages = messages
