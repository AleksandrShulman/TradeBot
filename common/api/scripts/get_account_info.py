import configparser
import os

from common.account.account import Account
from common.api.accounts.account_service import AccountService
from common.api.accounts.etrade.etrade_account_service import ETradeAccountService
from common.api.accounts.get_account_balance_request import GetAccountBalanceRequest
from common.api.accounts.get_account_info_request import GetAccountInfoRequest
from common.exchange.etrade.etrade_connector import ETradeConnector
from quotes.etrade.etrade_quote_service import ETradeQuoteService
from quotes.quote_service import QuoteService

"""
NOTE - To test in real life, it's necessary to include an `integration_test_properties.ini` file.
This file is in .gitignore, so as to not leak anyone's sensitive info when they commit code back.

An example is provided in `integration_test_properties.example.ini`.
"""

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'integration_test_properties.ini')
ACCOUNT_ID = 'ACCOUNT_ID'
ACCOUNT_ID_KEY = 'ACCOUNT_ID_KEY'

config = configparser.ConfigParser()

if __name__ == "__main__":
    config.read(CONFIG_FILE)
    connector: ETradeConnector = ETradeConnector()

    account_service: AccountService = ETradeAccountService(connector)

    #accounts: list[Account] = account_service.list_accounts().get_account_list()
    #account_id: str = config['ETRADE'][ACCOUNT_ID]
    #account_id_key: str = config['ETRADE'][ACCOUNT_ID_KEY]
    #account: Account = account_service.get_account_info(GetAccountInfoRequest(account_id)).account

    #print(accounts)
    #print(account)

    # now get the account balance
    different_account_id_key = '1XRq48Mv_HUiP8xmEZRPnA'
    get_balance_request = GetAccountBalanceRequest(different_account_id_key)
    response = account_service.get_account_balance(get_balance_request)
    balance = response.account_balance
    print(balance)
