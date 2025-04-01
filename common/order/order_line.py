from pydantic import BaseModel

from common.order.action import Action
from common.finance.tradable import Tradable

QUANTITY_FILLED_NOT_SPECIFIED = -1

class OrderLine(BaseModel):
    tradable: Tradable
    action: Action
    quantity: int
    quantity_filled: int = QUANTITY_FILLED_NOT_SPECIFIED

    @staticmethod
    def __validate__(quantity, action, tradable):
        # Factored this out of __init__...TODO: Use Pydantic to implement validation
        if not quantity or type(quantity) is not int or quantity < 1:
            raise Exception(f"Invalid value for quantity: {quantity}")

        if not action:
            raise Exception(f"Action required")

        if not tradable:
            raise Exception(f"Tradable required")



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