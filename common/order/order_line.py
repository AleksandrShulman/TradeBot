from common.order.action import Action
from common.finance.tradable import Tradable


class OrderLine:
    def __init__(self, tradable: Tradable, quantity: int, action: Action):
        if not quantity or type(quantity) is not int or quantity < 1:
            raise Exception(f"Invalid value for quantity: {quantity}")

        if not action:
            raise Exception(f"Action required")

        if not tradable:
            raise Exception(f"Tradable required")

        self.tradable = tradable
        self.quantity = quantity
        self.action = action

    def __str__(self):
        return f"{self.action}: {self.quantity} x {self.tradable}"
