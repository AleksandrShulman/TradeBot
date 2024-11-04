from common.finance.amount import Amount
from common.finance.price import Price
from common.finance.tradable import Tradable


class Equity(Tradable):
    def __init__(self, ticker, company_name):
        if not ticker or not company_name:
            raise Exception(f"Inputs ({ticker}, {company_name}) not valid")
        self.ticker = ticker
        self.company_name = company_name
        self.price: Price = None

    def set_price(self, price: Price):
        self.price = price

    def __str__(self):
        return f'{self.ticker}: {self.company_name}'
