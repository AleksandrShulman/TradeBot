from typing import Callable

from common.finance.amount import Amount
from common.finance.equity import Equity
from common.finance.options.order_analysis import OrderAnalysis
from common.order.action import Action
from common.order.order_price import OrderPrice
from common.order.order_type import OrderType


class EquityOrder(OrderAnalysis):
    def __init__(self, equity: Equity, quantity: float, action: Action, order_price: OrderPrice):
        self.equity = equity
        self.quantity = quantity
        self.action = action
        self.order_price = order_price
        super().__init__(self)

    def get_order_type(self) -> OrderType:
        return OrderType.EQ

    def get_collateral_required(self) -> Amount:
        pass