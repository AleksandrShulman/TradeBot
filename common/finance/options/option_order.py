from typing import Callable

from common.finance.amount import Amount
from common.finance.options.option_order_analysis import OptionOrderAnalysis
from common.finance.options.option_order_line import OptionOrderLine
from common.finance.options.order_analysis import OrderAnalysis
from common.order.expiry.good_for_day import GoodForDay
from common.order.order import Order
from common.order.order_price import OrderPrice
from common.order.order_type import OrderType

NAKED_CALL_REQUIRED_COLLATERAL_MULTIPLIER = 1.5

class OptionOrder(OptionOrderAnalysis):
    def __init__(self, order_price: OrderPrice, options: list[OptionOrderLine]):
        self.order_price = order_price
        self.options = options

    def to_order(self, expiry=GoodForDay()) -> Order:
        o: Order = Order(None, expiry, self.options, self.order_price)
        return o

    def get_value_at_expiry_function(self) -> Callable[[Amount], Amount]:
        pass

    def get_order_type(self) -> OrderType:
        pass

    """
    TODO: Build a Collateral Calculation Engine - a general solution that takes in some set of order lines instead of doing point calculations.
    Further, a proper CCE would take into account the existing portfolio (e.g. maybe there are some long puts that are helpful.
    A further improvement would be to make it a service and have it point out the least expensive ways to free up collateral (e.g. rolling
    long puts up and long calls down). 
    """
    def get_collateral_required(self) -> Amount:
        pass

    @staticmethod
    def from_order(o: Order):
        pass
