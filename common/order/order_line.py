from common.order.action import Action
from common.finance.tradable import Tradable


class OrderLine:
    def __init__(self, tradable: Tradable, action: Action, quantity: int, quantity_filled: int = 0):
        if not quantity or type(quantity) is not int or quantity < 1:
            raise Exception(f"Invalid value for quantity: {quantity}")

        if not action:
            raise Exception(f"Action required")

        if not tradable:
            raise Exception(f"Tradable required")

        self.tradable: Tradable = tradable
        self.action: Action = action
        self.quantity: int = quantity
        self.quantity_filled: int = quantity_filled

    def __str__(self):
        return f"{self.action}: {self.quantity} x {self.tradable}"

    def __hash__(self):
        return hash((self.tradable, self.action, self.quantity, self.quantity_filled))

    def __eq__(self, other):
        if self.tradable != other.tradable:
            return False
        if self.action != other.action:
            return False
        if self.quantity != other.quantity:
            return False
        if self.quantity_filled:
            if self.quantity_filled != other.quantity_filled:
                return False

        return True