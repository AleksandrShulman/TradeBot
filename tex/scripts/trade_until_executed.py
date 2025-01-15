import configparser
import datetime
import os

import pytest

from common.api.orders.etrade.etrade_order_service import ETradeOrderService
from common.api.orders.order_metadata import OrderMetadata
from common.api.orders.order_service import OrderService
from common.api.orders.preview_order_request import PreviewOrderRequest
from common.api.test.orders.order_test_util import OrderTestUtil
from common.exchange.etrade.etrade_connector import ETradeConnector
from common.finance.amount import Amount
from common.order.action import Action
from common.order.order import Order
from common.order.order_price_type import OrderPriceType
from quotes.api.get_tradable_request import GetTradableRequest
from quotes.api.get_tradable_response import GetTradableResponse
from quotes.etrade.etrade_quote_service import ETradeQuoteService
from quotes.quote_service import QuoteService

DEFAULT_WAIT: datetime.timedelta = datetime.timedelta(seconds=5)
DEFAULT_INITIAL_DELTA = Amount(0, 10)
DEFAULT_NO_BIDS_PRICE = Amount(0, 2)

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'integration_test_properties.ini')
ACCOUNT_ID_KEY = 'ACCOUNT_ID_KEY'

config = configparser.ConfigParser()

ZERO = Amount(0,0)

@pytest.fixture
def connector():
    config.read(CONFIG_FILE)
    connector: ETradeConnector = ETradeConnector()
    return connector

@pytest.fixture
def quote_service(connector):
    q: QuoteService = ETradeQuoteService(connector)
    return q

@pytest.fixture
def order_service(connector):
    o: OrderService = ETradeOrderService(connector)
    return o


def test_lower_until_executed(quote_service: QuoteService, order_service: OrderService):

    order = OrderTestUtil.build_spread_order()
    order_price = order.order_price
    order_market_price: Amount = get_market_price(order, quote_service)
    print(f"Security currently at: {order_market_price}")

    # Place order at $.05 MORE for SELL and $.05 LESS for BUY
    order_price.price = order_market_price + DEFAULT_INITIAL_DELTA if order_price.order_price_type is OrderPriceType.NET_CREDIT else order_market_price - DEFAULT_INITIAL_DELTA

    order_metadata: OrderMetadata = OrderMetadata()
    preview_order_request: PreviewOrderRequest = PreviewOrderRequest()
    order_service.preview_and_place_order
    # place the order




# This can also be done via a Bid-Ask - advantage is fewer API calls. Downside is relying on ETrade's order service
# This would be necessary to establish a first price for the order
def get_market_price(order: Order, quote_service: QuoteService)-> Amount:
    mark_to_market_price: float = 0
    for order_line in order.order_lines:
        get_tradable_request: GetTradableRequest = GetTradableRequest(order_line.tradable)
        get_tradable_response: GetTradableResponse = quote_service.get_tradable_quote(get_tradable_request)
        if get_tradable_response.current_price.bid == 0:
            # sometimes for thinly traded, far OTM options, the spreads are quite wide.
            # if the delta is >= $.10, we can just mark it as "$.02", since it takes at least $.01 to buy, and
            # these are often thinly traded, so we'll have to add a bit more.
            mark_to_market_price += DEFAULT_NO_BIDS_PRICE
        elif Action.is_long(order_line.action):
            mark_to_market_price += get_tradable_response.current_price.mark
        else:
            mark_to_market_price -= get_tradable_response.current_price.mark

    return Amount.from_float(mark_to_market_price)
