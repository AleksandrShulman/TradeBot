from abc import ABC
from datetime import datetime

from common.exchange.connector import Connector
from common.finance.option import Option
from quotes.api.tradable_request import TradableRequest
from quotes.api.tradable_response import TradableResponse


class QuoteService(ABC):

    def __init__(self, connector: Connector):
        self.connector = connector

    def get_tradable_quote(self, reqest: TradableRequest) -> TradableResponse:
        pass


    def get_equity_quote(self, symbol: str):
        # build request


        # parse response
        pass

    def get_options_chain_for_expiry(self, symbol: str, expiry: datetime):
        pass

    def get_option_details(self, option: Option):
        pass

