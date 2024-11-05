from common.exchange.etrade.etrade_connector import ETradeConnector


class ETradeOrderService():
    def __init__(self, connector: ETradeConnector):
        super().__init__(connector)
        self.session, self.base_url = self.connector.load_connection()