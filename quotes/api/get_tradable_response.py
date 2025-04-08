from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from common.api.finance.greeks.greeks import Greeks
from common.finance.price import Price
from common.finance.tradable import Tradable
from common.api.response import Response


class GetTradableResponse(Response, BaseModel):
    tradable: Tradable
    response_time: datetime
    current_price: Price
    volume: int
    greeks: Optional[Greeks] = None
