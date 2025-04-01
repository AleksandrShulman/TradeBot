import configparser
import copy
import json
import os
from datetime import datetime

import jsonpickle
import pytest

from common.api.encoding.custom_json_encoder import CustomJSONEncoder
from common.api.orders.OrderUtil import OrderUtil
from common.api.orders.cancel_order_request import CancelOrderRequest
from common.api.orders.cancel_order_response import CancelOrderResponse
from common.api.orders.etrade.etrade_order_service import ETradeOrderService
from common.api.orders.order_list_request import ListOrdersRequest
from common.api.orders.order_metadata import OrderMetadata
from common.api.orders.order_service import OrderService
from common.api.orders.place_modify_order_request import PlaceModifyOrderRequest
from common.api.orders.place_modify_order_response import PlaceModifyOrderResponse
from common.api.orders.place_order_request import PlaceOrderRequest
from common.api.orders.place_order_response import PlaceOrderResponse
from common.api.orders.preview_modify_order_request import PreviewModifyOrderRequest
from common.api.orders.preview_modify_order_response import PreviewModifyOrderResponse
from common.api.orders.preview_order_request import PreviewOrderRequest
from common.api.orders.preview_order_response import PreviewOrderResponse
from common.api.test.orders.order_test_util import OrderTestUtil
from common.exchange.etrade.etrade_connector import ETradeConnector
from common.finance.amount import Amount
from common.order.order import Order
from common.order.order_status import OrderStatus
from common.order.order_type import OrderType

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


def test_equity_order_for_preview_using_custom_json_encoder(order_service: OrderService, account_key: str):
    order_type: OrderType = OrderType.EQ
    account_id = account_key
    client_order_id = OrderUtil.generate_random_client_order_id()
    order_metadata: OrderMetadata = OrderMetadata(order_type, account_id, client_order_id)

    order = OrderTestUtil.build_equity_order()

    preview_order_request: PreviewOrderRequest = PreviewOrderRequest(order_metadata, order)

    result = json.dumps(preview_order_request, cls=CustomJSONEncoder)
    print(result)

    as_json = json.loads(result)
    assert as_json["order_metadata"]["client_order_id"] == client_order_id


def test_equity_order_for_preview_using_json_pickle(order_service: OrderService, account_key: str):
    order_type: OrderType = OrderType.EQ
    account_id = account_key
    client_order_id = OrderUtil.generate_random_client_order_id()
    order_metadata: OrderMetadata = OrderMetadata(order_type=order_type, account_id=account_id, client_order_id=client_order_id)

    order = OrderTestUtil.build_equity_order()

    preview_order_request: PreviewOrderRequest = PreviewOrderRequest(order_metadata=order_metadata, order=order)

    result = jsonpickle.encode(preview_order_request)
    print(result)

    decoded: PreviewOrderRequest = jsonpickle.decode(result)
    assert decoded.order_metadata.client_order_id == client_order_id


def test_equity_order_for_preview_using_pydantic(order_service: OrderService, account_key: str):
    order_type: OrderType = OrderType.EQ
    account_id = account_key
    client_order_id = OrderUtil.generate_random_client_order_id()
    order_metadata: OrderMetadata = OrderMetadata(order_type=order_type, account_id=account_id, client_order_id=client_order_id)

    order = OrderTestUtil.build_equity_order()

    preview_order_request: PreviewOrderRequest = PreviewOrderRequest(order_metadata=order_metadata, order=order)

    result: str = preview_order_request.model_dump_json()
    print(result)

    decoded: PreviewOrderRequest = PreviewOrderRequest.model_validate_json(result)
    assert decoded.order_metadata.client_order_id == client_order_id



def test_equity_order_for_preview_and_place(order_service: OrderService, account_key: str):
    order_type: OrderType = OrderType.EQ
    account_id = account_key
    client_order_id = OrderUtil.generate_random_client_order_id()
    order_metadata: OrderMetadata = OrderMetadata(order_type, account_id, client_order_id)

    order = OrderTestUtil.build_equity_order()

    preview_order_request: PreviewOrderRequest = PreviewOrderRequest(order_metadata, order)
    preview_order_response: PreviewOrderResponse = order_service.preview_order(preview_order_request)
    preview_id: str = preview_order_response.preview_id

    place_order_request: PlaceOrderRequest = PlaceOrderRequest(order_metadata, preview_id, order)
    place_order_response: PlaceOrderResponse = order_service.place_order(place_order_request)

    order_id = place_order_response.order_id
    assert order_id is not None

def test_equity_order_for_preview_place_and_cancel(order_service: OrderService, account_key: str):
    order_type: OrderType = OrderType.EQ
    account_id = account_key
    client_order_id = OrderUtil.generate_random_client_order_id()
    order_metadata: OrderMetadata = OrderMetadata(order_type, account_id, client_order_id)

    order = OrderTestUtil.build_equity_order()

    preview_order_request: PreviewOrderRequest = PreviewOrderRequest(order_metadata, order)
    preview_order_response: PreviewOrderResponse = order_service.preview_order(preview_order_request)
    preview_id: str = preview_order_response.preview_id

    place_order_request: PlaceOrderRequest = PlaceOrderRequest(order_metadata, preview_id, order)
    place_order_response: PlaceOrderResponse = order_service.place_order(place_order_request)

    order_id = place_order_response.order_id

    cancel_order_request: CancelOrderRequest = CancelOrderRequest(account_id, order_id)
    cancel_order_response: CancelOrderResponse = order_service.cancel_order(cancel_order_request)
    print(cancel_order_response)

def test_option_order_for_preview_and_place(order_service: OrderService, account_key: str):
    order_type: OrderType = OrderType.SPREADS
    account_id = account_key
    client_order_id = OrderUtil.generate_random_client_order_id()
    order_metadata: OrderMetadata = OrderMetadata(order_type, account_id, client_order_id)

    order = OrderTestUtil.build_spread_order()
    preview_order_request : PreviewOrderRequest = PreviewOrderRequest(order_metadata, order)
    preview_order_response: PreviewOrderResponse = order_service.preview_order(preview_order_request)

    preview_id = preview_order_response.preview_id

    place_order_request: PlaceOrderRequest = PlaceOrderRequest(order_metadata, preview_id, order)
    place_order_response: PlaceOrderResponse = order_service.place_order(place_order_request)
    print(place_order_response)

def test_option_order_for_preview_place_preview_modify_and_place_modify(order_service: OrderService, account_key: str):
    order_type: OrderType = OrderType.SPREADS
    account_id = account_key
    client_order_id = OrderUtil.generate_random_client_order_id()
    order_metadata: OrderMetadata = OrderMetadata(order_type, account_id, client_order_id)

    order = OrderTestUtil.build_spread_order()

    # Preview
    preview_order_request: PreviewOrderRequest = PreviewOrderRequest(order_metadata, order)
    preview_order_response: PreviewOrderResponse = order_service.preview_order(preview_order_request)

    preview_id = preview_order_response.preview_id

    # Place
    place_order_request: PlaceOrderRequest = PlaceOrderRequest(order_metadata, preview_id, order)
    place_order_response: PlaceOrderResponse = order_service.place_order(place_order_request)
    print(place_order_response)

    placed_order_id = place_order_response.order_id

    modified_order: Order = copy.deepcopy(place_order_response.order)
    modified_order.order_price.price = modified_order.order_price.price + Amount(0,5)

    # Regenerate client
    order_metadata.client_order_id = OrderUtil.generate_random_client_order_id()

    # Preview Modify
    preview_modify_order_request: PreviewModifyOrderRequest = PreviewModifyOrderRequest(order_metadata, placed_order_id, modified_order)
    preview_modify_order_response: PreviewModifyOrderResponse = order_service.preview_modify_order(preview_modify_order_request)

    modified_preview_id = preview_modify_order_response.preview_id

    # Place Modify
    place_modify_order_request: PlaceModifyOrderRequest = PlaceModifyOrderRequest(order_metadata, modified_preview_id, placed_order_id, modified_order)
    place_modify_order_response: PlaceModifyOrderResponse = order_service.place_modify_order(place_modify_order_request)

    assert place_modify_order_response.order_id is not None


def test_set_options_order_for_preview(order_service: OrderService, account_key: str):
    list_order_request = ListOrdersRequest(account_key, OrderStatus.OPEN, JAN_1_2024, TODAY, 50)
    orders = order_service.list_orders(list_order_request, dict())
    assert orders.order_list[0].placed_order_details.status == OrderStatus.OPEN

if __name__ == "__main__":
    pytest.main()