import datetime

from common.exchange.market_session import MarketSession
from common.finance.amount import Amount
from common.finance.currency import Currency
from common.finance.equity import Equity
from common.finance.option import Option
from common.finance.exercise_style import ExerciseStyle
from common.finance.option_type import OptionType
from common.finance.tradable import Tradable
from common.order.action import Action
from common.order.expiry.good_for_day import GoodForDay
from common.order.expiry.order_expiry import OrderExpiry
from common.order.order import Order
from common.order.order_line import OrderLine
from common.order.order_price import OrderPrice
from common.order.order_price_type import OrderPriceType
from common.order.order_status import OrderStatus

e: Equity = Equity("GE", "General Electric")


def test_build_single_line_order():
    strike: Amount = Amount(10,0, Currency.US_DOLLARS)

    account_id: str = 'abc987'
    order_id: int = 123
    order_expiry: OrderExpiry = GoodForDay()
    call_option: Tradable = Option(e, OptionType.CALL, strike, datetime.datetime(2024, 11, 5).date(), ExerciseStyle.AMERICAN)
    order_line = OrderLine(call_option, 1, Action.SELL_TO_OPEN)
    order_price: OrderPrice = OrderPrice(OrderPriceType.LIMIT_CREDIT, Amount(0, 14, Currency.US_DOLLARS))
    order_status: OrderStatus = OrderStatus.OPEN
    market_session: MarketSession = MarketSession.BOTH

    single_order = Order(account_id,  order_id,order_expiry, [order_line], order_price, order_status, market_session)

    assert single_order is not None


def test_build_dual_line_order():
    strike: Amount = Amount(10, 0, Currency.US_DOLLARS)

    account_id: str = 'abc987'
    order_id: int = 123
    order_expiry: OrderExpiry = GoodForDay()
    call_option: Tradable = Option(e, OptionType.CALL, strike, datetime.datetime(2024, 11, 5).date(),
                                   ExerciseStyle.AMERICAN)
    order_line = OrderLine(call_option, 2, Action.SELL_TO_OPEN)

    strike2: Amount = Amount(20, 0, Currency.US_DOLLARS)
    call_option2 = Option(e, OptionType.CALL, strike2, datetime.date(2024, 11, 5), ExerciseStyle.AMERICAN)
    order_line2 = OrderLine(call_option2, 1, Action.BUY_TO_OPEN)

    order_price: OrderPrice = OrderPrice(OrderPriceType.LIMIT_CREDIT, Amount(0, 14, Currency.US_DOLLARS))
    order_status: OrderStatus = OrderStatus.OPEN
    market_session: MarketSession = MarketSession.BOTH

    dual_order = Order(account_id, order_id, order_expiry, [order_line, order_line2], order_price, order_status, market_session)

    assert dual_order is not None