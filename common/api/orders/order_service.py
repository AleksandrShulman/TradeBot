from abc import ABC

from common.api.orders.cancel_order_request import CancelOrderRequest
from common.api.orders.cancel_order_response import CancelOrderResponse
from common.api.orders.get_order_request import GetOrderRequest
from common.api.orders.get_order_response import GetOrderResponse
from common.api.orders.order_list_request import ListOrdersRequest
from common.api.orders.order_list_response import ListOrdersResponse
from common.api.orders.place_modify_order_request import PlaceModifyOrderRequest
from common.api.orders.place_modify_order_response import PlaceModifyOrderResponse
from common.api.orders.place_order_request import PlaceOrderRequest
from common.api.orders.place_order_response import PlaceOrderResponse
from common.api.orders.preview_modify_order_request import PreviewModifyOrderRequest
from common.api.orders.preview_modify_order_response import PreviewModifyOrderResponse
from common.api.orders.preview_order_request import PreviewOrderRequest
from common.api.orders.preview_order_response import PreviewOrderResponse
from common.exchange.connector import Connector


class OrderService(ABC):
    def __init__(self, connector: Connector):
        self.connector = connector

    def list_orders(self, list_orders_request: ListOrdersRequest, exchange_specific_opts: dict[str, str]=None) -> ListOrdersResponse:
        pass

    def get_order(self, get_order_request: GetOrderRequest) -> GetOrderResponse:
        pass

    def cancel_order(self, cancel_order_request: CancelOrderRequest) -> CancelOrderResponse:
        pass

    def preview_modify_order(self, modify_order_request: PreviewModifyOrderRequest) -> PreviewModifyOrderResponse:
        pass

    def place_modify_order(self, modify_order_request: PlaceModifyOrderRequest) -> PlaceModifyOrderResponse:
        pass

    def preview_order(self, preview_order_request: PreviewOrderRequest) -> PreviewOrderResponse:
        pass

    def place_order(self, place_order_request: PlaceOrderRequest) -> PlaceOrderResponse:
        pass

    def preview_and_place_order(self, preview_order_request: PreviewOrderRequest):
        pass