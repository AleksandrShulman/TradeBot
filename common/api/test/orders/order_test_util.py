import string
from datetime import datetime
from random import choices

from common.exchange.market_session import MarketSession
from common.finance.amount import Amount
from common.finance.currency import Currency
from common.finance.equity import Equity
from common.finance.option import Option
from common.finance.option_type import OptionType
from common.order.action import Action
from common.order.expiry.good_for_day import GoodForDay
from common.order.order import Order
from common.order.order_line import OrderLine
from common.order.order_price import OrderPrice
from common.order.order_price_type import OrderPriceType


class OrderTestUtil:

    @staticmethod
    def build_equity_order():
        tradable: Equity = Equity("GE", "General Electric")
        ol_1 = OrderLine(tradable, Action.BUY, 5)
        order_price: OrderPrice = OrderPrice(OrderPriceType.LIMIT, Amount(100, 0))
        order_lines: list[OrderLine] = [ol_1]

        order = Order(None, GoodForDay(), order_lines, order_price, MarketSession.REGULAR)
        return order

    @staticmethod
    def build_spread_order():
        order_lines: list[OrderLine] = list()

        equity = Equity("GE", "General Electric")
        option_expiry: datetime.date = datetime(2025, 1, 31).date()
        tradable1: Option = Option(equity, OptionType.PUT, Amount(160, 0, Currency.US_DOLLARS), option_expiry)
        tradable2: Option = Option(equity, OptionType.PUT, Amount(155, 0, Currency.US_DOLLARS), option_expiry)

        ol_1 = OrderLine(tradable1, Action.SELL_OPEN, 1)
        ol_2 = OrderLine(tradable2, Action.BUY_OPEN, 1)

        order_price: OrderPrice = OrderPrice(OrderPriceType.NET_CREDIT, Amount(2, 49))

        order_lines.append(ol_1)
        order_lines.append(ol_2)

        return Order(None, GoodForDay(), order_lines, order_price, MarketSession.REGULAR)

    @staticmethod
    def generate_random_client_order_id():
        return "".join(choices(string.ascii_uppercase + string.digits, k=15))
