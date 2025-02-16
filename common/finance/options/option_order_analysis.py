from abc import ABC
from typing import Callable

from common.finance.amount import Amount
from common.finance.options.order_analysis import OrderAnalysis
from common.order.order_type import OrderType


class OptionOrderAnalysis(OrderAnalysis):
    def get_value_at_expiry_function(self) -> Callable[[Amount], Amount]:
        pass
