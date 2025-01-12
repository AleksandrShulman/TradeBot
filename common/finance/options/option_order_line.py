from typing import Callable

from common.finance.amount import Amount
from common.finance.option import Option
from common.order.action import Action
from common.order.order_line import OrderLine
from common.order.order_type import OrderType


class OptionOrderLine(OrderLine):
    def __init__(self, option: Option, action: Action,
                 quantity: int):
        if type(option) != Option:
            raise Exception(f"Cannot have an OptionOrderLine with type {type(option)}")
        super().__init__(option, action, quantity)
