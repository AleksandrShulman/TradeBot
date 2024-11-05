from common.exchange.market_session import MarketSession
from common.order.order_status import OrderStatus


class Trade:
    def __init__(self, account_id: str, trade_id: int, status: OrderStatus, market_session: MarketSession):
        self.account_id: str = account_id
        self.trade_id: int = trade_id
        self.status: OrderStatus = status
        self.market_session: MarketSession = market_session