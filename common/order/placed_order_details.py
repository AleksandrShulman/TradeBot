import datetime
from typing import Optional

from pydantic import BaseModel

from common.exchange.market_session import MarketSession
from common.finance.price import Price
from common.order.order_status import OrderStatus


class PlacedOrderDetails(BaseModel):
    account_id: str
    exchange_order_id: str
    status: OrderStatus
    order_placed_time: datetime.datetime
    current_market_price: Price
    market_session: Optional[MarketSession]
    replaces_order_id: Optional[str]
