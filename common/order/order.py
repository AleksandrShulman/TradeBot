from common.exchange.market_session import MarketSession
from common.finance.amount import Amount
from common.order.expiry.order_expiry import OrderExpiry
from common.order.order_line import OrderLine
from common.order.order_price import OrderPrice
from common.order.order_status import OrderStatus


class Order:
    def __init__(self, order_id: str, account_id: str, order_status: OrderStatus, expiry: OrderExpiry, order_lines: list[OrderLine],
                 order_price: OrderPrice, market_session: MarketSession, replaces_order_id: int = None):
        self.order_id: int = order_id
        self.account_id: str = account_id
        self.status: OrderStatus = order_status
        self.expiry = expiry
        self.order_lines = order_lines
        self.order_price: OrderPrice = order_price
        self.market_session: MarketSession = market_session
        self.replaces_order_id: int = replaces_order_id