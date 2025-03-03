from datetime import datetime
from unittest.mock import MagicMock

import pytest

from common.exchange.connector import Connector
from common.finance.amount import Amount
from common.finance.equity import Equity
from common.finance.option import Option
from common.finance.option_type import OptionType
from common.finance.price import Price
from common.finance.tradable import Tradable
from common.order.action import Action
from common.order.expiry.good_for_day import GoodForDay
from common.order.expiry.order_expiry import OrderExpiry
from common.order.order import Order
from common.order.order_line import OrderLine
from common.order.order_price import OrderPrice
from common.order.order_price_type import OrderPriceType
from quotes.api.get_tradable_request import GetTradableRequest
from quotes.api.get_tradable_response import GetTradableResponse
from quotes.quote_service import QuoteService
from oex.trade_execution_util import TradeExecutionUtil

equity = Equity("GE", "General Electric")

short_put = Option(equity, OptionType.PUT, Amount(195, 0), datetime(2025, 5, 16).date())
long_put = Option(equity, OptionType.PUT, Amount(185, 0), datetime(2025, 5, 16).date())

cs_short_put = Option(equity, OptionType.PUT, Amount(202, 50), datetime(2025, 2, 14).date())
cs_long_put = Option(equity, OptionType.PUT, Amount(197, 50), datetime(2025, 2, 21).date())
cs_long_put_2 = Option(equity, OptionType.PUT, Amount(195, 0), datetime(2025, 5, 14).date())


short_call = Option(equity, OptionType.CALL, Amount(200, 0), datetime(2025, 5, 16).date())
long_call = Option(equity, OptionType.CALL, Amount(210, 0), datetime(2025, 5, 16).date())

sell_put_order_line = OrderLine(short_put, Action.SELL_OPEN, 1)
buy_put_order_line = OrderLine(long_put, Action.BUY_OPEN, 1)

sell_call_order_line = OrderLine(short_call, Action.SELL_OPEN, 1)
buy_call_order_line = OrderLine(long_call, Action.BUY_OPEN, 1)

put_credit_spread_orderlines = [sell_put_order_line, buy_put_order_line]
call_credit_spread_orderlines = [sell_call_order_line, buy_call_order_line]



@pytest.fixture
def quote_service():
    # return a mock quote service
    c: Connector = Connector()
    qs: QuoteService = QuoteService(c)

    qs.get_tradable_quote = MagicMock(side_effect=return_market_prices)
    return qs

def test_put_credit_spread(quote_service):
    order: Order = Order(None, GoodForDay(), put_credit_spread_orderlines, OrderPrice(OrderPriceType.NET_CREDIT, Amount(3, 18)))

    market_price: Price = TradeExecutionUtil.get_market_price(order, quote_service)

    assert market_price.bid == 2.30
    assert market_price.ask == 4.05
    assert market_price.mark == 3.17

def test_call_credit_spread(quote_service):
    order: Order = Order(None, GoodForDay(), call_credit_spread_orderlines, OrderPrice(OrderPriceType.NET_CREDIT, Amount(5, 28)))

    market_price: Price = TradeExecutionUtil.get_market_price(order, quote_service)

    assert market_price.bid == 4.65
    assert market_price.ask == 5.90
    assert market_price.mark == 5.28

def test_put_debit_spread(quote_service):
    cs_short_put_order_line = OrderLine(cs_short_put, Action.SELL_OPEN, 1)
    cs_long_put_order_line = OrderLine(cs_long_put, Action.BUY_OPEN, 1)
    cs_long_put_2_order_line = OrderLine(cs_long_put_2, Action.BUY_OPEN, 1)

    call_debit_spread_order_lines = [cs_short_put_order_line, cs_long_put_order_line, cs_long_put_2_order_line]
    order: Order = Order(None, GoodForDay(), call_debit_spread_order_lines,
                         OrderPrice(OrderPriceType.NET_CREDIT, Amount(0, 7)))

    market_price: Price = TradeExecutionUtil.get_market_price(order, quote_service)

    assert market_price.bid == .42
    assert market_price.ask == -.29
    assert market_price.mark == .07


# If python had a proper mocking framework, this contrivance wouldn't be necessary
def return_market_prices(get_tradable_request: GetTradableRequest)->GetTradableResponse:
    if get_tradable_request == GetTradableRequest(short_put):
        return GetTradableResponse(get_tradable_request.tradable, None, Price(Amount(7, 15).to_float(),Amount (8, 30).to_float()), 5)
    elif get_tradable_request == GetTradableRequest(long_put):
        return GetTradableResponse(get_tradable_request.tradable, None, Price(Amount(4, 25).to_float(),Amount (4, 85).to_float()), 5)
    elif get_tradable_request == GetTradableRequest(short_call):
        return GetTradableResponse(get_tradable_request.tradable, None, Price(Amount(15, 20).to_float(), Amount(15, 75).to_float()), 5)
    elif get_tradable_request == GetTradableRequest(long_call):
        return GetTradableResponse(get_tradable_request.tradable, None, Price(Amount(9, 85).to_float(), Amount(10, 55).to_float()), 5)
    elif get_tradable_request == GetTradableRequest(cs_short_put):
        return GetTradableResponse(get_tradable_request.tradable, None, Price(Amount(3, 20).to_float(), Amount(3, 50).to_float()), 5)
    elif get_tradable_request == GetTradableRequest(cs_long_put):
        return GetTradableResponse(get_tradable_request.tradable, None, Price(Amount(1, 99).to_float(), Amount(2, 30).to_float()), 5)
    elif get_tradable_request == GetTradableRequest(cs_long_put_2):
        return GetTradableResponse(get_tradable_request.tradable, None, Price(Amount(1, 9).to_float(), Amount(1, 19).to_float()), 5)
    else:
        raise Exception("Option not recognized")