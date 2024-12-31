from abc import ABC

from common.api.orders.cancel_order_request import CancelOrderRequest
from common.api.orders.cancel_order_response import CancelOrderResponse
from common.api.orders.get_order_request import GetOrderRequest
from common.api.orders.get_order_response import GetOrderResponse
from common.api.orders.order_list_request import OrderListRequest
from common.api.orders.order_list_response import OrderListResponse
from common.api.orders.place_orders_request import PlaceOrdersRequest
from common.api.orders.place_orders_response import PlaceOrdersResponse
from common.api.orders.preview_orders_request import PreviewOrdersRequest
from common.api.orders.preview_orders_response import PreviewOrdersResponse
from common.exchange.connector import Connector


class OrderService(ABC):
    def __init__(self, connector: Connector):
        self.connector = connector

    def list_orders(self, list_orders_request: OrderListRequest, exchange_specific_opts: dict[str, str]) -> OrderListResponse:
        pass

    def get_order(self, get_order_request: GetOrderRequest) -> GetOrderResponse:
        pass

    def cancel_order(self, cancel_order_request: CancelOrderRequest) -> CancelOrderResponse:
        pass

    def preview_orders(self, preview_order_request: PreviewOrdersRequest) -> PreviewOrdersResponse:
        pass

    def place_order(self, place_order_request: PlaceOrdersRequest) -> PlaceOrdersResponse:
        pass