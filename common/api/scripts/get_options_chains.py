import configparser
import datetime
import os

import pytest

from common.api.portfolio.GetPortfolioRequest import GetPortfolioRequest
from common.api.portfolio.GetPortfolioResponse import GetPortfolioResponse
from common.api.portfolio.etrade.etrade_portfolio_service import ETradePortfolioService
from common.exchange.etrade.etrade_connector import ETradeConnector
from common.finance.equity import Equity
from quotes.api.get_option_expire_dates_request import GetOptionExpireDatesRequest
from quotes.api.get_option_expire_dates_response import GetOptionExpireDatesResponse
from quotes.api.get_options_chain_request import GetOptionsChainRequest
from quotes.api.get_options_chain_response import GetOptionsChainResponse
from quotes.etrade.etrade_quote_service import ETradeQuoteService
from quotes.quote_service import QuoteService

"""
NOTE - To test in real life, it's necessary to include an `integration_test_properties.ini` file.
This file is in .gitignore, so as to not leak anyone's sensitive info when they commit code back.

An example is provided in `integration_test_properties.example.ini`.
"""

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'integration_test_properties.ini')
ACCOUNT_ID_KEY = 'ACCOUNT_ID_KEY'

ticker = "SPY"
equity_name = "SPDR S&P 500 ETF TRUST"

equity: Equity = Equity(ticker, equity_name)

config = configparser.ConfigParser()

@pytest.fixture
def q():
    config.read(CONFIG_FILE)

    connector: ETradeConnector = ETradeConnector()
    return ETradeQuoteService(connector)

def test_option_expirations(q: QuoteService):
    req: GetOptionExpireDatesRequest = GetOptionExpireDatesRequest(ticker)
    resp: GetOptionExpireDatesResponse = q.get_option_expire_dates(req)

    print(resp.expire_dates)

def test_options_chains(q: QuoteService):

    expiry = datetime.datetime(2025, 3, 21).date()

    options_chain_request_for_date: GetOptionsChainRequest = GetOptionsChainRequest(equity, expiry)
    options_chain_request_no_expiry: GetOptionsChainRequest = GetOptionsChainRequest(equity, None)

    get_options_chain_response: GetOptionsChainResponse = q.get_options_chain(options_chain_request_for_date)
    options_chain = get_options_chain_response.options_chain
    print(options_chain)

    # If no date is provided, it will default to today's date. May possible default to the next closing date.
    get_options_chain_response_no_expiry: GetOptionsChainResponse = q.get_options_chain(options_chain_request_no_expiry)
    options_chain_no_expiry = get_options_chain_response_no_expiry.options_chain
    print(options_chain_no_expiry)