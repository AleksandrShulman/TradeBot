from datetime import datetime

from common.finance.option import Option
from common.finance.price import Price
from common.finance.tradable import Tradable
from common.order.tradable_type import TradableType


class PricedOption(Tradable):
    def __init__(self, option: Option, current_price: Price):
        self.option = option
        self.price: Price = current_price

        for var in vars(self):
            if self.__getattribute__(var) is None:
                raise Exception(f"Missing var! - {var}")

    def get_type(self) ->TradableType:
        return TradableType.Option

    def copy_of(self):
        return PricedOption(self.option, self.price)
