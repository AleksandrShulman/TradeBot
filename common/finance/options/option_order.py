from typing import Callable

from common.finance.amount import Amount
from common.finance.options.option_order_line import OptionOrderLine
from common.order.order_price import OrderPrice
from common.order.order_type import OrderType

NAKED_CALL_REQUIRED_COLLATERAL_MULTIPLIER = 1.5

class OptionOrder:
    def __init__(self, order_price: OrderPrice, options: list[OptionOrderLine]):
        self.order_price = order_price
        self.options = options

    def get_value_at_expiry_function(self) -> Callable[[Amount], Amount]:
        pass

    def get_order_type(self) -> OrderType:
        pass

    def get_collateral_required(self) -> Amount:
        pass