import configparser
import datetime
import os

from common.api.portfolio.GetPortfolioRequest import GetPortfolioRequest
from common.api.portfolio.GetPortfolioResponse import GetPortfolioResponse
from common.api.portfolio.etrade.etrade_portfolio_service import ETradePortfolioService
from common.exchange.etrade.etrade_connector import ETradeConnector
from common.finance.equity import Equity
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

config = configparser.ConfigParser()

if __name__ == "__main__":
    config.read(CONFIG_FILE)

    connector: ETradeConnector = ETradeConnector()
    q: QuoteService = ETradeQuoteService(connector)

    account_id_key = config['ETRADE'][ACCOUNT_ID_KEY]
    ticker = "SPY"
    equity_name = "SPDR S&P 500 ETF TRUST"

    equity: Equity = Equity(ticker, equity_name)

    expiry = datetime.datetime(2025, 3, 21).date()

    options_chain_request_for_date: GetOptionsChainRequest = GetOptionsChainRequest(equity, expiry)

    get_options_chain_response: GetOptionsChainResponse = q.get_options_chain(options_chain_request_for_date)

    options_chain = get_options_chain_response.options_chain

    print(options_chain)