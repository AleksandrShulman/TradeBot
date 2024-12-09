
from common.order.executed_order_details import ExecutionOrderDetails
from common.order.order import Order


class ExecutedOrder:
    def __init__(self, order: Order, execution_order_details: ExecutionOrderDetails):
        self.order = order
        self.execution_details = execution_order_details

    def get_order(self):
        return self.order