from common.finance.price import Price
from common.finance.tradable import Tradable


class Equity(Tradable):
    def __init__(self, ticker, company_name:str=None):
        if not ticker:
            raise Exception(f"Inputs ({ticker} not valid")
        self.ticker = ticker
        self.company_name = company_name
        self.price: Price = None

    def set_price(self, price: Price):
        self.price = price

    def __hash__(self):
        return hash(self.ticker)

    def __eq__(self, other):
        return self.ticker == other.ticker

    def __str__(self):
        return f'{self.ticker}: {self.company_name}'
