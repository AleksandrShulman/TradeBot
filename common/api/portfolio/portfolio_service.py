from abc import ABC

from common.api.portfolio.GetPortfolioRequest import GetPortfolioRequest
from common.exchange.connector import Connector


class PortfolioService(ABC):

    def __init__(self, connector: Connector):
        self.connector = connector

    def list_portfolios(self):
        pass

    def get_portfolio_info(self, get_portfolio_request: GetPortfolioRequest):
        pass
    pass