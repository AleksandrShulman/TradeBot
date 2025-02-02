from common.finance.price import Price
from common.order.tradable_type import TradableType


class Tradable:
    def set_price(self, price: Price):
        self.price: Price = price

    def get_type(self)->TradableType:
        pass