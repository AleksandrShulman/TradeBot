import datetime

from common.exchange.market_session import MarketSession
from common.order.expiry.order_expiry import OrderExpiry
from common.order.order_line import OrderLine
from common.order.order_price import OrderPrice


class Order:
    def __init__(self, order_id: str, expiry: OrderExpiry, order_lines: list[OrderLine],
                 order_price: OrderPrice, market_session: MarketSession, client_order_id=None):
        self.order_id: str = order_id
        self.expiry = expiry
        self.order_lines = order_lines
        self.order_price: OrderPrice = order_price
        self.market_session: MarketSession = market_session
        if client_order_id:
            self.client_order_id = client_order_id