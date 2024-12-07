from common.api.orders.get_order_request import GetOrderRequest
from common.api.orders.get_order_response import GetOrderResponse
from common.api.orders.order_list_request import OrderListRequest
from common.api.orders.order_list_response import OrderListResponse
from common.api.orders.order_service import OrderService
from common.api.orders.place_order_request import PlaceOrderRequest
from common.api.orders.place_order_response import PlaceOrderResponse
from common.exchange.etrade.etrade_connector import ETradeConnector
from common.order.order import Order


class ETradeOrderService(OrderService):
    def __init__(self, connector: ETradeConnector):
        super().__init__(connector)
        self.session, self.base_url = self.connector.load_connection()

    def list_orders(self, list_orders_request: OrderListRequest, exchange_specific_opts: dict[str, str]) -> OrderListResponse:
        #account_id = list_orders_request.account_id
        account_id = list_orders_request.account_id
        path = f"/v1/accounts/{account_id}/orders.json"
        count = list_orders_request.count

        params = dict()
        params["count"] = count
        params["fromDate"] = list_orders_request.from_date.strftime("%m%d%Y")
        params["toDate"] = list_orders_request.to_date.strftime("%m%d%Y")

        if exchange_specific_opts:
            for k, v in list_orders_request.items():
                params[k] = v

        url = self.base_url + path
        print(url)
        response = self.session.get(url, params=params)

        order_list_response = ETradeOrderService._parse_order_list_response(response)
        return order_list_response

    def get_order(self, get_order_request: GetOrderRequest) -> GetOrderResponse:
        pass

    def place_order(self, place_order_request: PlaceOrderRequest) -> PlaceOrderResponse:
        pass

    @staticmethod
    def _parse_order_list_response(response) -> list[Order]:
        print(response)
        pass