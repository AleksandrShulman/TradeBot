from common.api.request import Request
from common.order.order import Order
from oex.managed_order_execution import ManagedOrderExecution


class GetOrderExecutionResponse(Request):
    def __init__(self, managed_order_execution: ManagedOrderExecution):
        self.managed_order_execution: ManagedOrderExecution = managed_order_execution


