from abc import ABC
from typing import Callable

from common.finance.amount import Amount
from common.order.order_type import OrderType


class OrderAnalysis(ABC):
    def get_order_type(self) -> OrderType:
        pass

    def get_collateral_required(self) -> Amount:
        pass