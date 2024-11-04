import configparser
import os

from common.api.accounts.account_service import AccountService
from common.api.accounts.etrade.etrade_account_service import ETradeAccountService
from common.api.accounts.get_account_info_request import GetAccountInfoRequest
from common.api.portfolio.GetPortfolioRequest import GetPortfolioRequest
from common.api.portfolio.GetPortfolioResponse import GetPortfolioResponse
from common.api.portfolio.etrade.etrade_portfolio_service import ETradePortfolioService
from common.exchange.etrade.etrade_connector import ETradeConnector
from quotes.etrade.etrade_quote_service import ETradeQuoteService
from quotes.quote_service import QuoteService

"""
NOTE - To test in real life, it's necessary to include an `integration_test_properties.ini` file.
This file is in .gitignore, so as to not leak anyone's sensitive info when they commit code back.

An example is provided in `integration_test_properties.example.ini`.
"""

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'integration_test_properties.ini')
ACCOUNT_ID_KEY = 'ACCOUNT_ID'

config = configparser.ConfigParser()

if __name__ == "__main__":
    config.read(CONFIG_FILE)

    connector: ETradeConnector = ETradeConnector()
    q: QuoteService = ETradeQuoteService(connector)

    portfolio_service: ETradePortfolioService = ETradePortfolioService(connector)

    account_key = config['ETRADE'][ACCOUNT_ID_KEY]
    portfolio_request: GetPortfolioRequest = GetPortfolioRequest(account_key)
    get_portfolio_response: GetPortfolioResponse = portfolio_service.get_portfolio_info(portfolio_request)

    portfolio = get_portfolio_response.portfolio

    print(portfolio)