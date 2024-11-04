from datetime import datetime

from common.finance.option import Option
from common.finance.price import Price


class PricedOption(Option):
    def __init__(self, option: Option, current_price: Price):
        self.option = option
        self.price: Price = current_price

        for var in vars(self):
            if self.__getattribute__(var) is None:
                raise Exception(f"Missing var! - {var}")

    def copy_of(self):
        return PricedOption(self.equity, self.type, self.strike, self.expiry, self.price, self.style)
