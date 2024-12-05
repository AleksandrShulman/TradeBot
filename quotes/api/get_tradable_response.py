from datetime import datetime

from common.finance.price import Price
from common.finance.tradable import Tradable
from common.api.response import Response


class GetTradableResponse(Response):
    def __init__(self, tradable: Tradable, response_time: datetime, current_price: Price, volume: int):
        self.tradable: Tradable = tradable
        self.response_time = response_time
        self.current_price: Price = current_price
        self.volume: int = volume
