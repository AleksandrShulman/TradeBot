from common.order.order_price import OrderPrice
from common.order.order_status import OrderStatus


class ManagedOrderExecution:
    def __init__(self, managed_order_execution_id: str, exchange_order_id, status: OrderStatus, latest_order_price: OrderPrice):
        self.managed_order_execution_id: str = managed_order_execution_id
        self.exchange_order_id: str = exchange_order_id
        self.status: OrderStatus = status
        self.latest_order_price: OrderPrice = latest_order_price