import configparser
import datetime
import os
from time import sleep

import pytest

from common.api.orders.cancel_order_request import CancelOrderRequest
from common.api.orders.cancel_order_response import CancelOrderResponse
from common.api.orders.etrade.etrade_order_service import ETradeOrderService
from common.api.orders.get_order_request import GetOrderRequest
from common.api.orders.get_order_response import GetOrderResponse
from common.api.orders.order_metadata import OrderMetadata
from common.api.orders.order_service import OrderService
from common.api.orders.place_order_response import PlaceOrderResponse
from common.api.orders.preview_order_request import PreviewOrderRequest
from common.api.test.orders.order_test_util import OrderTestUtil
from common.exchange.etrade.etrade_connector import ETradeConnector
from common.finance.amount import Amount
from common.finance.equity import Equity
from common.order.action import Action
from common.order.order_price_type import OrderPriceType
from common.order.order_status import OrderStatus
from common.order.order_type import OrderType
from common.order.placed_order import PlacedOrder
from quotes.etrade.etrade_quote_service import ETradeQuoteService
from quotes.quote_service import QuoteService
from tex.tactics.incremental_price_delta_execution_tactic import IncrementalPriceDeltaExecutionTactic
from tex.trade_execution_util import TradeExecutionUtil

DEFAULT_WAIT: datetime.timedelta = datetime.timedelta(seconds=5)
DEFAULT_INITIAL_DELTA = Amount(0, 25)

CONFIG_FILE = os.path.join(os.path.dirname(__file__),'../../common/api/scripts/', 'integration_test_properties.ini')
ACCOUNT_ID_KEY = 'ACCOUNT_ID_KEY'

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

SFIX = Equity("SFIX", "STITCH FIX INC COM CL A")

ZERO = Amount(0,0)

@pytest.fixture
def connector():
    return ETradeConnector()

@pytest.fixture
def quote_service(connector):
    q: QuoteService = ETradeQuoteService(connector)
    return q

@pytest.fixture
def order_service(connector):
    o: OrderService = ETradeOrderService(connector)
    return o

@pytest.fixture
def account_id()->str:
    return config['ETRADE'][ACCOUNT_ID_KEY]

def test_lower_until_executed(account_id: str, quote_service: QuoteService, order_service: OrderService):

    # The pattern is we'll put in the order, to get a sense of the actual price, once the response returns. From there, we'll keep getting new prices until it's clsoed.
    # Get a sense of what it may be worth
    order = OrderTestUtil.build_equity_order(equity=SFIX, action=Action.BUY)
    order_market_price: Amount = TradeExecutionUtil.get_market_price(order, quote_service)
    print(f"Security currently at: {order_market_price}")

    # Find a price that's reasonable
    potential_order_price: Amount = order_market_price + DEFAULT_INITIAL_DELTA if order.order_price.order_price_type is OrderPriceType.NET_CREDIT else order_market_price - DEFAULT_INITIAL_DELTA
    order.order_price.price = potential_order_price

    client_order_id = OrderTestUtil.generate_random_client_order_id()
    order_metadata: OrderMetadata = OrderMetadata(order.get_order_type(), account_id, client_order_id)
    preview_order_request: PreviewOrderRequest = PreviewOrderRequest(order_metadata, order)

    # place the order
    place_order_response: PlaceOrderResponse = order_service.preview_and_place_order(preview_order_request)
    order_id = place_order_response.order_id

    adjust_order_until_executed(account_id, order_id, order_service, quote_service)


def adjust_order_until_executed(account_id: str, order_id: str, order_service: OrderService, quote_service: QuoteService):
        # Get information about the order
        get_order_response: GetOrderResponse = order_service.get_order(GetOrderRequest(account_id, order_id))
        placed_order = get_order_response.placed_order
        order_type: OrderType = placed_order.order.get_order_type()
        order = placed_order.order

        while placed_order.placed_order_details.status == OrderStatus.OPEN:
            print("Cancelling old order")
            cancel_order_request: CancelOrderRequest = CancelOrderRequest(account_id, order_id)
            response: CancelOrderResponse = order_service.cancel_order(cancel_order_request)
            print(f"Cancelled old order {response.order_id}")

            new_price, wait_period = IncrementalPriceDeltaExecutionTactic.new_price(placed_order, quote_service)
            order.order_price.price = new_price
            order_metadata: OrderMetadata = OrderMetadata(order_type, account_id, OrderTestUtil.generate_random_client_order_id())
            preview_order_request: PreviewOrderRequest = PreviewOrderRequest(order_metadata, order)

            # place the order
            print("Submitted new order")
            response: PlaceOrderResponse = order_service.preview_and_place_order(preview_order_request)
            print(f"New order is {response.order_id}")
            order_id = response.order_id

            order_status = order_service.get_order(
                GetOrderRequest(account_id, order_id)).placed_order.placed_order_details.status
            print(f"Order status {response.order_id}: {order_status}")
            if order_status == OrderStatus.EXECUTED:
                print("Awesome, it executed!")
                break

            print(f"Sleeping {wait_period} seconds before adding new order")
            sleep(wait_period)