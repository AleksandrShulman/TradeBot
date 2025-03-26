from flask import Flask

from common.api.orders.etrade.etrade_order_service import ETradeOrderService
from common.api.orders.order_list_request import ListOrdersRequest
from common.api.orders.order_service import OrderService
from common.exchange.connector import Connector
from common.exchange.etrade.etrade_connector import ETradeConnector
from common.exchange.exchange_name import ExchangeName
from quotes.etrade.etrade_quote_service import ETradeQuoteService
from quotes.quote_service import QuoteService


class OexService:

    def __init__(self):
        self._app = Flask(OexService.__name__)
        self._register_endpoints()
        self._obtain_credentials()

    @property
    def app(self) -> Flask:
        return self._app

    @app.setter
    def app(self, app: Flask):
        self._app = app

    def _register_endpoints(self):
        self.app.add_url_rule(rule='/', endpoint='root', view_func=self.get_root, methods=['GET'])
        self.app.add_url_rule(rule='/health-check', endpoint='health-check', view_func=self.health_check, methods=['GET'])
        self.app.add_url_rule(rule='/api/v1/<exchange>/orders', endpoint='list-orders', view_func=self.list_orders, methods=['GET'])

    def _obtain_credentials(self):
        self.connectors: dict[str, Connector] = dict()
        etrade_connector: ETradeConnector = ETradeConnector().load_connection()
        self.connectors["etrade"] = etrade_connector

    def _setup_exchange_services(self):
        self.order_services: dict[str, OrderService] = dict()
        self.quote_services: dict[str, QuoteService] = dict()

        etrade_key: str = self.connectors[ExchangeName.ETRADE.value]
        etrade_order_service = ETradeOrderService(etrade_key)
        etrade_quote_service = ETradeQuoteService(etrade_key)

        self.order_services[etrade_key] = etrade_order_service
        self.quote_services[etrade_key] = etrade_quote_service

    def run(self, *args, **kwargs):
        self.app.run(*args, **kwargs)

    @staticmethod
    def health_check():
        return "OEX Service Up"

    @staticmethod
    def get_root():
        return "OEX Service"

    @staticmethod
    def list_orders(self, exchange):
        order_service: OrderService = self.order_services[exchange]
        list_order_request = ListOrdersRequest()
        order_service.list_orders()
        return f"Getting orders for {exchange}"

if __name__ == "__main__":
    from waitress import serve

    # Login To Exchange Here
    oex_app = OexService()
    oex_app.run(host="0.0.0.0", port=8080)