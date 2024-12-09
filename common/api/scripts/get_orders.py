import configparser
import os
from datetime import datetime

import pytest

from common.api.orders.etrade.etrade_order_service import ETradeOrderService
from common.api.orders.order_list_request import OrderListRequest
from common.api.orders.order_service import OrderService
from common.exchange.etrade.etrade_connector import ETradeConnector
from common.order.executed_order import ExecutedOrder
from common.order.order_status import OrderStatus

"""
NOTE - To test in real life, it's necessary to include an `integration_test_properties.ini` file.
This file is in .gitignore, so as to not leak anyone's sensitive info when they commit code back.

An example is provided in `integration_test_properties.example.ini`.
"""

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'integration_test_properties.ini')
ACCOUNT_ID_KEY = 'ACCOUNT_ID_KEY'

JAN_1_2024 = datetime(2024,1,1).date()
JAN_2_2024 = datetime(2024,1,2).date()

TODAY = datetime.now().date()
MAX_COUNT = 1000

config = configparser.ConfigParser()

@pytest.fixture
def account_key():
    return config['ETRADE'][ACCOUNT_ID_KEY]

@pytest.fixture
def order_service():
    config.read(CONFIG_FILE)
    connector: ETradeConnector = ETradeConnector()
    o: OrderService = ETradeOrderService(connector)
    return o

def test_get_date_range_orders_within_range(order_service: OrderService, account_key: str):
    start_date = JAN_1_2024
    end_date = JAN_2_2024

    list_order_request = OrderListRequest(account_key, OrderStatus.ANY, start_date, end_date, 50)
    orders = order_service.list_orders(list_order_request, dict())

    for order in orders.order_list:
        if type(order) == ExecutedOrder:
            order = order.get_order()
        assert start_date <= order.order_placed_time.date() <= end_date

def test_get_open_orders(order_service: OrderService, account_key: str):
    list_order_request = OrderListRequest(account_key, OrderStatus.OPEN, JAN_1_2024, TODAY, 50)
    orders = order_service.list_orders(list_order_request, dict())
    assert orders.order_list[0].status == OrderStatus.OPEN

def test_get_all_orders(order_service: OrderService, account_key: str):
    list_order_request = OrderListRequest(account_key, OrderStatus.ANY, JAN_1_2024, TODAY, 50)
    orders = order_service.list_orders(list_order_request, dict())
    assert len(orders.order_list) == 50

if __name__ == "__main__":
    pytest.main()