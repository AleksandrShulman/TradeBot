from datetime import datetime


class GetOptionsChainRequest:
    def __init__(self, symbol: str, expiry: datetime.date):
        # Perhaps a date will also be required
        self.symbol = symbol
        self.expiry: datetime.date = expiry