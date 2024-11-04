from common.finance.price import Price


class Tradable:
    def set_price(self, price: Price):
        self.price: Price = price
