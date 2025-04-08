from datetime import datetime

from pydantic import BaseModel

from common.finance.option import Option
from common.finance.price import Price
from common.finance.tradable import Tradable
from common.order.tradable_type import TradableType


class PricedOption(Tradable):
    option: Option

    def copy_of(self):
        return PricedOption(option=self.option, price=self.price)
