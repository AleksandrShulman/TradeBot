from datetime import datetime

import jsonpickle
from flask import Flask, jsonify, make_response
from flask import request

from common.api.encoding.custom_json_provider import CustomJSONProvider
from common.api.orders.etrade.etrade_order_service import ETradeOrderService
from common.api.orders.get_order_request import GetOrderRequest
from common.api.orders.get_order_response import GetOrderResponse
from common.api.orders.order_list_request import ListOrdersRequest
from common.api.orders.order_list_response import ListOrdersResponse
from common.api.orders.order_metadata import OrderMetadata
from common.api.orders.order_service import OrderService
from common.api.orders.place_order_request import PlaceOrderRequest
from common.api.orders.place_order_response import PlaceOrderResponse
from common.api.orders.preview_order_request import PreviewOrderRequest
from common.api.orders.preview_order_response import PreviewOrderResponse
from common.exchange.connector import Connector
from common.exchange.etrade.etrade_connector import ETradeConnector
from common.exchange.exchange_name import ExchangeName
from common.order.order import Order
from common.order.order_status import OrderStatus
from quotes.etrade.etrade_quote_service import ETradeQuoteService
from quotes.quote_service import QuoteService

JAN_1_2024 = datetime(2024,1,1).date()
DEFAULT_START_DATE = JAN_1_2024
DEFAULT_COUNT = 100


class OexService:

    def __init__(self):
        self._app = Flask(OexService.__name__)
        self._app.json_provider_class = CustomJSONProvider(self._app)  # Tell Flask to use the custom encoder
        self._app.json = CustomJSONProvider(self._app)
        self._register_endpoints()
        self._obtain_credentials()
        self._setup_exchange_services()

    @property
    def app(self) -> Flask:
        return self._app

    @app.setter
    def app(self, app: Flask):
        self._app = app

    def _register_endpoints(self):
        self.app.add_url_rule(rule='/', endpoint='root', view_func=self.get_root, methods=['GET'])
        self.app.add_url_rule(rule='/health-check', endpoint='health-check', view_func=self.health_check, methods=['GET'])
        self.app.add_url_rule(rule='/api/v1/<exchange>/<account_id>/orders', endpoint='list-orders', view_func=self.list_orders, methods=['GET'])
        self.app.add_url_rule(rule='/api/v1/<exchange>/<account_id>/orders/<order_id>', endpoint='get-order',
                              view_func=self.get_order, methods=['GET'])

        self.app.add_url_rule(rule='/api/v1/<exchange>/<account_id>/orders/preview', endpoint='preview-order',
                              view_func=self.preview_order, methods=['POST'])

        self.app.add_url_rule(rule='/api/v1/<exchange>/<account_id>/orders/preview/<preview_id>', endpoint='place-order',
                              view_func=self.place_order, methods=['POST'])

        self.app.add_url_rule(rule='/api/v1/<exchange>/<account_id>/orders/preview_and_place', endpoint='preview-and-place-order',
                              view_func=self.preview_and_place_order, methods=['POST'])

    def _obtain_credentials(self):
        self.connectors: dict[ExchangeName, Connector] = dict()
        etrade_connector: ETradeConnector = ETradeConnector()
        self.connectors[ExchangeName.ETRADE] = etrade_connector

    def _setup_exchange_services(self):
        self.order_services: dict[ExchangeName, OrderService] = dict()
        self.quote_services: dict[ExchangeName, QuoteService] = dict()

        # E*Trade
        etrade_key: ExchangeName = ExchangeName.ETRADE
        etrade_connector: ETradeConnector = self.connectors[ExchangeName.ETRADE]
        etrade_order_service = ETradeOrderService(etrade_connector)
        etrade_quote_service = ETradeQuoteService(etrade_connector)

        self.order_services[etrade_key] = etrade_order_service
        self.quote_services[etrade_key] = etrade_quote_service

        # TODO: Add for IKBR and Schwab


    def run(self, *args, **kwargs):
        self.app.run(*args, **kwargs)

    @staticmethod
    def health_check():
        return "OEX Service Up"

    @staticmethod
    def get_root():
        return "OEX Service"


    def list_orders(self, exchange: str, account_id: str):
        args = request.args
        status_str = args.get('status')
        status = OrderStatus.ANY if not status_str else OrderStatus[status_str]
        from_date = DEFAULT_START_DATE if not 'from_date' in args else datetime.datetime.strptime(args.get('from_date'), '%yyyy-mm-dd').date()
        to_date = datetime.today().date() if not 'to_date' in args else datetime.datetime.strptime(args.get('to_date'), '%yyyy-mm-dd').date()

        count = args.get('count') if 'count' in args else DEFAULT_COUNT

        order_service: OrderService = self.order_services[ExchangeName[exchange.upper()]]
        list_order_request = ListOrdersRequest(account_id, status, from_date, to_date, count)

        resp: ListOrdersResponse = order_service.list_orders(list_order_request)

        return jsonify(resp)

    def get_order(self, exchange: str, account_id: str, order_id: str):
        if not order_id:
            # TODO: Factor this out
            # TODO: Put HTTP response codes in an eum
            resp = make_response(f"Order {order_id} not found", 400)
            resp.headers['X-Something'] = 'A value'
            return resp

        order_service: OrderService = self.order_services[ExchangeName[exchange.upper()]]
        get_order_request = GetOrderRequest(account_id=account_id, order_id=order_id)

        resp: GetOrderResponse = order_service.get_order(get_order_request)

        return jsonify(resp)

    def preview_order(self, exchange, account_id: str):
        content_type = request.headers.get('Content-Type')
        if (content_type != 'application/json'):
            return 'Content-Type not supported!'

        preview_order_request = PreviewOrderRequest.model_validate(request.json)
        if not preview_order_request.order_metadata.account_id:
            preview_order_request.order_metadata.account_id = account_id

        order_service: OrderService = self.order_services[ExchangeName[exchange.upper()]]
        response: PreviewOrderResponse = order_service.preview_order(preview_order_request)

        return jsonify(response)

    def place_order(self, exchange, account_id: str, preview_id: str):
        content_type = request.headers.get('Content-Type')
        if (content_type != 'application/json'):
            return 'Content-Type not supported!'

        place_order_request = PlaceOrderRequest.model_validate(request.json)
        if not place_order_request.order_metadata.account_id:
            place_order_request.order_metadata.account_id = account_id

        place_order_request.preview_id = preview_id

        order_service: OrderService = self.order_services[ExchangeName[exchange.upper()]]
        response: PlaceOrderResponse = order_service.place_order(place_order_request)

        return jsonify(response)

    def preview_and_place_order(self, exchange, account_id: str):
        content_type = request.headers.get('Content-Type')
        if (content_type != 'application/json'):
            return 'Content-Type not supported!'

        preview_order_request = PreviewOrderRequest.model_validate(request.json)
        if not preview_order_request.order_metadata.account_id:
            preview_order_request.order_metadata.account_id = account_id

        order_service: OrderService = self.order_services[ExchangeName[exchange.upper()]]
        preview_order_response: PreviewOrderResponse = order_service.preview_order(preview_order_request)
        preview_id = preview_order_response.preview_id

        order_metadata: OrderMetadata = preview_order_request.order_metadata
        order: Order = preview_order_request.order

        place_order_request: PlaceOrderRequest = PlaceOrderRequest(order_metadata=order_metadata, preview_id=preview_id,
                                                                   order=order)
        place_order_response: PlaceOrderResponse = order_service.place_order(place_order_request)
        return jsonify(place_order_response)

if __name__ == "__main__":
    from waitress import serve

    # Login To Exchange Here
    oex_app = OexService()
    oex_app.run(host="0.0.0.0", port=8080)