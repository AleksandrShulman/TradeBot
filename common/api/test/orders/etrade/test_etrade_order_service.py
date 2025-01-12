import os
import pickle

import pytest
from unittest.mock import MagicMock, patch

from rauth import OAuth1Session

from common.api.orders.etrade.etrade_order_service import ETradeOrderService
from common.api.orders.order_metadata import OrderMetadata
from common.api.orders.place_order_response import PlaceOrderResponse
from common.api.orders.preview_order_request import PreviewOrderRequest
from common.api.orders.preview_order_response import PreviewOrderResponse
from common.api.test.orders.order_test_util import OrderTestUtil
from common.exchange.etrade.etrade_connector import ETradeConnector, DEFAULT_ETRADE_BASE_URL_FILE
from common.finance.amount import Amount
from common.finance.currency import Currency
from common.finance.equity import Equity
from common.order.action import Action
from common.order.expiry.good_for_day import GoodForDay
from common.order.order import Order
from common.order.order_line import OrderLine
from common.order.order_price import OrderPrice
from common.order.order_price_type import OrderPriceType
from common.order.order_type import OrderType


# TODO: Adjust this suite to do both XML and JSON inputs ..
# For some endpoints, I wasn't able to get the JSON input to work

ACCOUNT_ID = "account123"

CLIENT_ORDER_ID = "ABC123"
SPREAD_ORDER_PREVIEW_ID = "2060570516106"
SPREAD_ORDER_TOTAL_ORDER_VALUE = Amount(247,95, negative=True)
SPREAD_ORDER_ESTIMATED_COMMISSION = Amount(1,0)

SPREAD_ORDER_METADATA = OrderMetadata(OrderType.SPREADS, ACCOUNT_ID, CLIENT_ORDER_ID)

PLACED_ORDER_ID = 81117

SPREAD_PREVIEW_ORDER_RESPONSE_FILE = os.path.join(os.path.dirname(__file__), "./resources/output_preview_order_spread")
SPREAD_PLACE_ORDER_RESPONSE_FILE = os.path.join(os.path.dirname(__file__), "./resources/output_place_order_spread")

SPREAD_ORDER = OrderTestUtil.build_spread_order()
SPREAD_ORDER.order_id_to_modify = PLACED_ORDER_ID

@pytest.fixture
def preview_request()->PreviewOrderRequest:
    tradable = Equity("GE", "General Electric")
    order_line = OrderLine(tradable, Action.BUY, 3)
    order_price = OrderPrice(OrderPriceType.NET_DEBIT, Amount(100,0,Currency.US_DOLLARS))
    order = Order(None, GoodForDay(), [order_line], order_price)

    order_metadata: OrderMetadata = OrderMetadata(OrderType.EQ, ACCOUNT_ID, CLIENT_ORDER_ID)

    return PreviewOrderRequest(order_metadata, order)

@pytest.fixture
def preview_order_spread_response():
    return _read_input(SPREAD_PREVIEW_ORDER_RESPONSE_FILE)


@pytest.fixture
def place_order_spread_response():
    return _read_input(SPREAD_PLACE_ORDER_RESPONSE_FILE)


@pytest.fixture
@patch('rauth.OAuth1Session')
def connector(session: OAuth1Session):
    # build a connector that gives back a mock session
    connector: ETradeConnector = ETradeConnector()
    connector.load_connection = MagicMock(return_value = (session, DEFAULT_ETRADE_BASE_URL_FILE))
    return connector

@pytest.fixture
def order_service(connector):
    # TODO: Set up the service that will provide mock responses to given requests
    return ETradeOrderService(connector)

def test_process_spread_preview_order_response(preview_order_spread_response):
    response: PreviewOrderResponse = ETradeOrderService._parse_preview_order_response(preview_order_spread_response, SPREAD_ORDER_METADATA)
    assert SPREAD_ORDER_PREVIEW_ID == str(response.preview_id)
    assert SPREAD_ORDER_TOTAL_ORDER_VALUE == response.preview_order_info.total_order_value
    assert SPREAD_ORDER_ESTIMATED_COMMISSION == response.preview_order_info.estimated_commission

def test_process_spread_place_order_response_id_parsed(place_order_spread_response):
    response: PlaceOrderResponse = ETradeOrderService._parse_place_order_response(place_order_spread_response, SPREAD_ORDER_METADATA, SPREAD_ORDER_PREVIEW_ID)
    assert PLACED_ORDER_ID == response.order_id

def test_process_spread_place_order_response_order_parsed(place_order_spread_response):
    response: PlaceOrderResponse = ETradeOrderService._parse_place_order_response(place_order_spread_response, SPREAD_ORDER_METADATA, SPREAD_ORDER_PREVIEW_ID)
    assert SPREAD_ORDER == response.order

def test_preview_spread_order(order_service, preview_request, preview_order_spread_response):
    # Given a mock service
    session = order_service.session
    session.post = MagicMock(return_value = preview_order_spread_response)

    # Given a Request
    response: PreviewOrderResponse = order_service.preview_order(preview_request)

    # Assert output makes sense
    assert SPREAD_ORDER_PREVIEW_ID == str(response.preview_id)

def test_place_order():
    # Given an order that has been previewed

    # When a user makes place request to the service

    # Assert that the place response is handled correctly
    pass

def test_cancel_placed_order():
    # Given an order that has been placed

    # When a user cancels that order

    # That the cancellation response is processed correctly

    pass

def test_modify_order_preview():
    pass

def test_place_modified_order():
    pass

def _read_input(input_file):
    with open(input_file, 'rb') as handle:
        response = pickle.load(handle)
    return response

if __name__ == "__main__":
    pass