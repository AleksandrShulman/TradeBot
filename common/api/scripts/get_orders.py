import configparser
import os
from datetime import datetime

from common.api.accounts.account_service import AccountService
from common.api.accounts.etrade.etrade_account_service import ETradeAccountService
from common.api.accounts.get_account_info_request import GetAccountInfoRequest
from common.api.orders.etrade.etrade_order_service import ETradeOrderService
from common.api.orders.order_list_request import OrderListRequest
from common.api.orders.order_service import OrderService
from common.exchange.etrade.etrade_connector import ETradeConnector
from common.order.order_status import OrderStatus

"""
NOTE - To test in real life, it's necessary to include an `integration_test_properties.ini` file.
This file is in .gitignore, so as to not leak anyone's sensitive info when they commit code back.

An example is provided in `integration_test_properties.example.ini`.
"""

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'integration_test_properties.ini')
ACCOUNT_ID_KEY = 'ACCOUNT_ID'

JAN_1_2024 = datetime(2024,1,1).date()
TODAY = datetime.now().date()
MAX_COUNT = 1000

config = configparser.ConfigParser()

if __name__ == "__main__":
    config.read(CONFIG_FILE)
    connector: ETradeConnector = ETradeConnector()
    o: OrderService = ETradeOrderService(connector)
    account_key = config['ETRADE'][ACCOUNT_ID_KEY]

    list_order_request = OrderListRequest(account_key, OrderStatus.OPEN, JAN_1_2024, TODAY, 1000 )
    orders = o.list_orders(list_order_request, None)

    print(orders)