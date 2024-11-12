from abc import ABC

from common.api.orders.get_order_request import GetOrderRequest
from common.api.orders.get_order_response import GetOrderResponse
from common.api.orders.order_list_request import OrderListRequest
from common.api.orders.order_list_response import OrderListResponse
from common.api.orders.place_order_request import PlaceOrderRequest
from common.api.orders.place_order_response import PlaceOrderResponse
from common.exchange.connector import Connector


class OrderService(ABC):
    def __init__(self, connector: Connector):
        self.connector = connector

    def list_orders(self, list_orders_request: OrderListRequest, exchange_specific_opts: dict[str, str]) -> OrderListResponse:
        pass

    def get_order(self, get_order_request: GetOrderRequest) -> GetOrderResponse:
        pass

    def place_order(self, place_order_request: PlaceOrderRequest) -> PlaceOrderResponse:
        pass