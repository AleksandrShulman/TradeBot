from common.api.orders.OrderPlacementMessage import OrderPlacementMessage


class ETradeOrderResponseMessage(OrderPlacementMessage):
    def __init__(self, code: str, description: str, message_type:str):
        super().__init__(description)
        self.code = code
        self.type = message_type