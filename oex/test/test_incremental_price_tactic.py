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
from common.order.order_price import OrderPrice
from common.order.order_price_type import OrderPriceType
from common.order.order_status import OrderStatus
from common.order.placed_order import PlacedOrder
from common.order.placed_order_details import PlacedOrderDetails
from oex.tactics.incremental_price_delta_execution_tactic import IncrementalPriceDeltaExecutionTactic


ORDER_PRICE_EXACTLY_200 = Amount(200, 0)
ORDER_PRICE_EXACTLY_100: Amount = Amount(100, 0)

MARKET_PRICE_NEAR_125 = Price(124.95, 125.05)

THIRTY_CENTS: Price = Price(.28, .32)

SIXTY_CENTS_AMT: Amount = Amount(0, 60)
EXACTLY_SIXTY_CENTS: Amount = Amount(0, 60)

CREDIT_SIXTY_CENTS = OrderPrice(OrderPriceType.NET_CREDIT, SIXTY_CENTS_AMT)
DEBIT_SIXTY_CENTS = OrderPrice(OrderPriceType.NET_DEBIT, EXACTLY_SIXTY_CENTS)

NINETY_CENTS_MARKET_PRICE: Price = Price(-.85, -.95)

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

def get_equity_order_response(action: Action, current_order_price: Amount, current_market_price_equity: Price):
    equity_order: Order = OrderTestUtil.build_equity_order(action=action, price=current_order_price)

    placed_order_details: PlacedOrderDetails = PlacedOrderDetails("account1", "123", OrderStatus.OPEN, datetime.datetime.now(), current_market_price_equity)
    placed_order: PlacedOrder = PlacedOrder(equity_order, placed_order_details)
    return GetOrderResponse(placed_order)

def get_spread_order_response(current_order_price: OrderPrice, current_market_price: Price):
    equity_order: Order = OrderTestUtil.build_spread_order(order_price=current_order_price)
    placed_order_details: PlacedOrderDetails = PlacedOrderDetails("account1", "123", OrderStatus.OPEN, datetime.datetime.now(), current_market_price)
    placed_order: PlacedOrder = PlacedOrder(equity_order, placed_order_details)
    return GetOrderResponse(placed_order)

def test_equity_order_price_less_than_market_price_debit():
    placed_order = get_equity_order_response(Action.BUY, ORDER_PRICE_EXACTLY_100, MARKET_PRICE_NEAR_125).placed_order
    new_price, _ = IncrementalPriceDeltaExecutionTactic.new_price(placed_order)

    assert new_price.price == Amount(108,33)
    assert new_price.order_price_type == OrderPriceType.LIMIT

def test_spread_order_price_more_than_market_price_credit():
    placed_order = get_spread_order_response(current_order_price=CREDIT_SIXTY_CENTS, current_market_price=THIRTY_CENTS).placed_order
    new_price, _ = IncrementalPriceDeltaExecutionTactic.new_price(placed_order)

    assert new_price.order_price_type == OrderPriceType.NET_CREDIT
    assert new_price.price == Amount(0,50)

def test_spread_order_price_less_than_market_price_debit():
    placed_order = get_spread_order_response(DEBIT_SIXTY_CENTS, NINETY_CENTS_MARKET_PRICE).placed_order
    new_price, _ = IncrementalPriceDeltaExecutionTactic.new_price(placed_order)

    assert new_price.price == Amount(0,70, negative=False)
    assert new_price.order_price_type == OrderPriceType.NET_DEBIT

def test_equity_order_price_more_than_market_price_credit():
    placed_order = get_equity_order_response(Action.SELL, ORDER_PRICE_EXACTLY_200, MARKET_PRICE_NEAR_125).placed_order
    new_price, _ = IncrementalPriceDeltaExecutionTactic.new_price(placed_order)

    assert new_price.price == Amount(175,0)
    assert new_price.order_price_type == OrderPriceType.LIMIT

def test_equity_order_price_increments_by_one_when_near_mark_to_market():
    placed_order = get_equity_order_response(Action.SELL, Amount(124,96), MARKET_PRICE_NEAR_125).placed_order
    new_price, _ = IncrementalPriceDeltaExecutionTactic.new_price(placed_order)

    assert new_price.price == Amount(124, 95)

    placed_order.order.order_price.price = new_price.price
    new_price, _ = IncrementalPriceDeltaExecutionTactic.new_price(placed_order)

    assert new_price.price == Amount(124, 94)
    assert new_price.order_price_type == OrderPriceType.LIMIT