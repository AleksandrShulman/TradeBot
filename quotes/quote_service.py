from abc import ABC
from datetime import datetime

from common.exchange.connector import Connector
from common.finance.option import Option
from quotes.api.get_option_expire_dates_request import GetOptionExpireDatesRequest
from quotes.api.get_option_expire_dates_response import GetOptionExpireDatesResponse
from quotes.api.get_options_chain_request import GetOptionsChainRequest
from quotes.api.get_options_chain_response import GetOptionsChainResponse
from quotes.api.get_tradable_request import GetTradableRequest
from quotes.api.get_tradable_response import GetTradableResponse


class QuoteService(ABC):

    def __init__(self, connector: Connector):
        self.connector = connector

    def get_tradable_quote(self, request: GetTradableRequest) -> GetTradableResponse:
        pass

    def get_option_expire_dates(self, get_options_expire_dates_request: GetOptionExpireDatesRequest) -> GetOptionExpireDatesResponse:
        pass

    def get_equity_quote(self, symbol: str):
        pass

    def get_options_chain(self, get_options_chain_request: GetOptionsChainRequest) -> GetOptionsChainResponse:
        pass

    def get_option_details(self, option: Option):
        pass

