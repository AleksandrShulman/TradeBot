from common.finance.tradable import Tradable
from common.api.request import Request


class TradableRequest(Request):
    def __init__(self, tradable: Tradable):
        self.tradable = tradable

    def get_tradable(self):
        return self.tradable