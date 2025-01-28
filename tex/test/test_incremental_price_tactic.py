import datetime
from unittest.mock import patch, MagicMock

import pytest
from rauth import OAuth1Session

from common.api.orders.etrade.etrade_order_service import ETradeOrderService
from common.api.orders.get_order_response import GetOrderResponse
from common.api.test.orders.order_test_util import OrderTestUtil
from common.exchange.etrade.etrade_connector import ETradeConnector, DEFAULT_ETRADE_BASE_URL_FILE
from common.finance.amount import Amount
from common.finance.price import Price
from common.order.action import Action
from common.order.order import Order
from common.order.order_status import OrderStatus
from common.order.placed_order import PlacedOrder
from common.order.placed_order_details import PlacedOrderDetails
from tex.scripts.trade_until_executed import get_market_price
from tex.tactics.incremental_price_delta_execution_tactic import IncrementalPriceDeltaExecutionTactic


@pytest.fixture
@patch('rauth.OAuth1Session')
def connector(session: OAuth1Session):
    # build a connector that gives back a mock session
    connector: ETradeConnector = ETradeConnector()
    connector.load_connection = MagicMock(return_value=(session, DEFAULT_ETRADE_BASE_URL_FILE))
    return connector

@pytest.fixture
def order_service(connector):
    # TODO: Set up the service that will provide mock responses to given requests
    return ETradeOrderService(connector)

def get_order_response(action: Action, current_order_price: Amount, current_market_price_equity: Price):
    equity_order: Order = OrderTestUtil.build_equity_order(action, current_order_price)
    placed_order_details: PlacedOrderDetails = PlacedOrderDetails("account1", "123", OrderStatus.OPEN, datetime.datetime.now(), current_market_price_equity)
    placed_order: PlacedOrder = PlacedOrder(equity_order, placed_order_details)
    return GetOrderResponse(placed_order)

def test_order_price_less_than_market_price_debit():
    MARKET_PRICE_NEAR_125: Price = Price(124.95, 125.05)
    ORDER_PRICE_EXACTLY_100: Amount = Amount(100, 0)

    placed_order = get_order_response(Action.BUY, ORDER_PRICE_EXACTLY_100, MARKET_PRICE_NEAR_125).placed_order
    new_price: Amount = IncrementalPriceDeltaExecutionTactic.new_price(placed_order)

    assert new_price == Amount(108,33)


def test_order_price_more_than_market_price_credit():
    MARKET_PRICE_NEAR_125 = Price(124.95, 125.05)
    ORDER_PRICE_EXACTLY_200 = Amount(200, 0)

    placed_order = get_order_response(Action.SELL, ORDER_PRICE_EXACTLY_200, MARKET_PRICE_NEAR_125).placed_order
    new_price: Amount = IncrementalPriceDeltaExecutionTactic.new_price(placed_order)

    assert new_price == Amount(175, 0)