from common.finance.price import Price
from common.finance.tradable import Tradable
from common.order.tradable_type import TradableType


class Equity(Tradable):
    ticker: str
    company_name: str
    price: Price = None

    class Config:
        arbitrary_types_allowed = True

    def set_price(self, price: Price):
        self.price = price

    def get_type(self) ->TradableType:
        return TradableType.Equity

    def __hash__(self):
        return hash(self.ticker)

    def __eq__(self, other):
        return self.ticker == other.ticker

    def __str__(self):
        return f'{self.ticker}: {self.company_name}'
