from common.api.orders.order_placement_message import OrderPlacementMessage


class ETradeOrderResponseMessage(OrderPlacementMessage):
    code: str
    message_type: str
