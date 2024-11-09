from common.exchange.market_session import MarketSession
from common.order.expiry.order_expiry import OrderExpiry
from common.order.order_line import OrderLine
from common.order.order_price import OrderPrice
from common.order.order_status import OrderStatus


class Order:
    def __init__(self, account_id: str, order_id: int, expiry: OrderExpiry, order_lines: list[OrderLine],
                 order_price: OrderPrice, order_status: OrderStatus, market_session: MarketSession):
        self.account_id: str = account_id
        self.order_id: int = order_id
        self.status: OrderStatus = order_status
        self.expiry = expiry
        self.order_lines = order_lines
        self.order_price = order_price
        self.market_session: MarketSession = market_session

