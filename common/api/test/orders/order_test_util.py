import string
from collections import deque
from datetime import datetime
from random import choices
from xml.sax import default_parser_list

from pygments.lexer import default

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

DEFAULT_AMOUNT = Amount(100, 0)

class OrderTestUtil:

    @staticmethod
    def build_equity_order(action=Action.BUY, price: Amount = DEFAULT_AMOUNT):
        tradable: Equity = Equity("GE", "General Electric")
        ol_1 = OrderLine(tradable, action, 5)
        order_price: OrderPrice = OrderPrice(OrderPriceType.LIMIT, price)
        order_lines: list[OrderLine] = [ol_1]

        order = Order(None, GoodForDay(), order_lines, order_price)
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

        return Order(None, GoodForDay(), order_lines, order_price)

    @staticmethod
    def build_covered_call():
        order_lines: list[OrderLine] = list()

        equity = Equity("SFIX", "STITCH FIX INC COM CL A")
        option_expiry: datetime.date = datetime(2025, 1, 31).date()
        tradable1: Option = Option(equity, OptionType.CALL, Amount(4, 0, Currency.US_DOLLARS), option_expiry)

        ol_1 = OrderLine(equity, Action.BUY, 100)
        ol_2 = OrderLine(tradable1, Action.SELL_OPEN, 1)

        order_price: OrderPrice = OrderPrice(OrderPriceType.NET_DEBIT, Amount(3, 84))

        order_lines.append(ol_1)
        order_lines.append(ol_2)

        return Order(None, GoodForDay(), order_lines, order_price)

    @staticmethod
    def build_calendar_spread():
        order_lines: list[OrderLine] = list()

        equity = Equity("SFIX", "STITCH FIX INC COM CL A")
        option_expiry_1: datetime.date = datetime(2025, 1, 31).date()
        option_expiry_2: datetime.date = datetime(2025, 6, 20).date()
        tradable1: Option = Option(equity, OptionType.CALL, Amount(4, 0, Currency.US_DOLLARS), option_expiry_1)
        tradable2: Option = Option(equity, OptionType.CALL, Amount(4, 0, Currency.US_DOLLARS), option_expiry_2)

        ol_1 = OrderLine(tradable1, Action.SELL_OPEN, 1)
        ol_2 = OrderLine(tradable2, Action.BUY_OPEN, 1)

        order_price: OrderPrice = OrderPrice(OrderPriceType.NET_DEBIT, Amount(0, 45))

        order_lines.append(ol_1)
        order_lines.append(ol_2)

        return Order(None, GoodForDay(), order_lines, order_price)

    @staticmethod
    def build_three_option_put_one_spread_one_naked():
        order_lines: list[OrderLine] = list()

        equity = Equity("SFIX", "STITCH FIX INC COM CL A")
        option_expiry_1: datetime.date = datetime(2025, 1, 31).date()
        tradable1: Option = Option(equity, OptionType.CALL, Amount(5, 0, Currency.US_DOLLARS), option_expiry_1)
        tradable2: Option = Option(equity, OptionType.CALL, Amount(3, 0, Currency.US_DOLLARS), option_expiry_1)

        ol_1 = OrderLine(tradable1, Action.SELL_OPEN, 2)
        ol_2 = OrderLine(tradable2, Action.BUY_OPEN, 1)

        order_price: OrderPrice = OrderPrice(OrderPriceType.NET_DEBIT, Amount(0, 45))

        order_lines.append(ol_1)
        order_lines.append(ol_2)

        return Order(None, GoodForDay(), order_lines, order_price)

    @staticmethod
    def build_diagonal_spread():
        order_lines: list[OrderLine] = list()

        equity = Equity("SFIX", "STITCH FIX INC COM CL A")
        option_expiry_1: datetime.date = datetime(2025, 1, 31).date()
        option_expiry_2: datetime.date = datetime(2025, 6, 20).date()
        tradable1: Option = Option(equity, OptionType.CALL, Amount(4, 0, Currency.US_DOLLARS), option_expiry_1)
        tradable2: Option = Option(equity, OptionType.CALL, Amount(5, 0, Currency.US_DOLLARS), option_expiry_2)

        ol_1 = OrderLine(tradable1, Action.SELL_OPEN, 1)
        ol_2 = OrderLine(tradable2, Action.BUY_OPEN, 1)

        order_price: OrderPrice = OrderPrice(OrderPriceType.NET_DEBIT, Amount(0, 45))

        order_lines.append(ol_1)
        order_lines.append(ol_2)

        return Order(None, GoodForDay(), order_lines, order_price)


    @staticmethod
    def build_horizontal_spread():
        order_lines: list[OrderLine] = list()

        equity = Equity("SFIX", "STITCH FIX INC COM CL A")
        option_expiry: datetime.date = datetime(2025, 1, 31).date()
        tradable1: Option = Option(equity, OptionType.CALL, Amount(4, 0, Currency.US_DOLLARS), option_expiry)
        tradable2: Option = Option(equity, OptionType.CALL, Amount(5, 0, Currency.US_DOLLARS), option_expiry)


        ol_1 = OrderLine(tradable1, Action.SELL_OPEN, 1)
        ol_2 = OrderLine(tradable2, Action.BUY_OPEN, 1)

        order_price: OrderPrice = OrderPrice(OrderPriceType.NET_CREDIT, Amount(0, 45))

        order_lines.append(ol_1)
        order_lines.append(ol_2)

        return Order(None, GoodForDay(), order_lines, order_price)

    @staticmethod
    def generate_random_client_order_id():
        return "".join(choices(string.ascii_uppercase + string.digits, k=15))
