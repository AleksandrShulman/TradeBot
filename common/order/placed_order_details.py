import datetime

from common.order.order_status import OrderStatus


class PlacedOrderDetails:
    def __init__(self, account_id: str, exchange_order_id, status: OrderStatus, order_placed_time: datetime, replaces_order_id: str=None):
        self.account_id: str = account_id
        self.exchange_order_id = exchange_order_id
        self.status: OrderStatus = status
        self.order_placed_time: datetime.datetime = order_placed_time
        self.replaces_order_id: str = replaces_order_id