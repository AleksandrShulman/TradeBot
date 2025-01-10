import copy
import datetime

from common.exchange.market_session import MarketSession
from common.order.expiry.order_expiry import OrderExpiry
from common.order.order_line import OrderLine
from common.order.order_price import OrderPrice


class Order:
    def __init__(self, order_id: str, expiry: OrderExpiry, order_lines: list[OrderLine],
                 order_price: OrderPrice, market_session: MarketSession=MarketSession.REGULAR):
        # This is the Local Order Id.
        self.order_id: str = order_id
        self.expiry: OrderExpiry = expiry
        self.order_lines: list[OrderLine] = order_lines
        self.order_price: OrderPrice = order_price
        self.market_session: MarketSession = market_session

    def __eq__(self, other):
        if self.order_id != other.order_id:
            return False
        if self.expiry != other.expiry:
            return False
        if self.order_price != other.order_price:
            return False
        if self.market_session != other.market_session:
            return False
        if len(self.order_lines) != len(other.order_lines):
            return False
        ols = set[OrderLine]()
        for order_line in other.order_lines:
            ols.add(order_line)
        for order_line in self.order_lines:
            if order_line not in ols:
                return False

        return True

    def __copy__(self):
        return Order(self.order_id, self.expiry, copy.deepcopy(self.order_lines), self.order_price, self.market_session)