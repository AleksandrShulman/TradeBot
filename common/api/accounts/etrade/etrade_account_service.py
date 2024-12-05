from datetime import datetime

from common.account.account import Account
from common.account.account_balance import AccountBalance
from common.account.computed_balance import ComputedBalance
from common.account.etrade.ETradeAccount import ETradeAccount
from common.account.option_level import OptionLevel
from common.api.accounts.account_list_response import AccountListResponse
from common.api.accounts.account_service import AccountService
from common.api.accounts.get_account_balance_request import GetAccountBalanceRequest
from common.api.accounts.get_account_balance_response import GetAccountBalanceResponse
from common.api.accounts.get_account_info_request import GetAccountInfoRequest
from common.api.accounts.get_account_info_response import GetAccountInfoResponse
from common.exchange.etrade.etrade_connector import ETradeConnector


DEFAULT_INST_TYPE = "BROKERAGE"

class ETradeAccountService(AccountService):

    def __init__(self, connector: ETradeConnector):
        super().__init__(connector)
        self.session, self.base_url = self.connector.load_connection()

    def list_accounts(self) -> AccountListResponse:
        path = f"/v1/accounts/list.json"
        url = self.base_url + path
        response = self.session.get(url)
        account_list_response = ETradeAccountService._parse_account_list_response(response)
        return AccountListResponse(account_list_response)

    def get_account_balance(self, get_account_info_request: GetAccountBalanceRequest) -> GetAccountBalanceResponse:
        account_id = get_account_info_request.account_id
        path = f"/v1/accounts/{account_id}/balance.json?instType={DEFAULT_INST_TYPE}&realTimeNAV=true"
        url = self.base_url + path
        response = self.session.get(url)
        print(response.request.headers)
        print(response.url)

        account_balance: AccountBalance = ETradeAccountService._parse_account_balance_response(response)

        return GetAccountBalanceResponse(account_balance)


    def get_account_info(self, get_account_info_request: GetAccountInfoRequest) -> GetAccountInfoResponse:
        path = f"/v1/accounts/list.json"
        url = self.base_url + path
        response = self.session.get(url)
        print(response.request.headers)
        print(response.url)

        name_filter = (lambda a: a.account_id == get_account_info_request.account_id)

        account_list: list[Account] = ETradeAccountService._parse_account_list_response(response, name_filter)
        if len(account_list) > 1:
            raise Exception("More than one result")

        if len(account_list) == 1:
            return GetAccountInfoResponse(account_list[0])

        return GetAccountInfoResponse(None)

    @staticmethod
    def _parse_account_list_response(input, f=(lambda a: a)) -> list[Account]:
        data: dict = input.json()
        if 'error' in data:
            code = data['error']['code']
            message = data['error']['message']
            raise Exception(f"Error from E*Trade: {code}: {message}")
        account_list_response = data["AccountListResponse"]
        accounts: list = account_list_response["Accounts"]

        return_accounts = map(lambda account: ETradeAccount(account["accountId"], account["accountIdKey"],
                                                    account["accountName"], account["accountDesc"]), accounts["Account"])

        return list(filter(f, return_accounts))

    @staticmethod
    def _parse_account_balance_response(input) -> AccountBalance:
        data: dict = input.json()
        if 'Error' in data:
            message = data['Error']['message']
            raise Exception(f"Error from E*Trade: {input.status_code}: {message}")


        account_id = data["accountId"]
        as_of_date = datetime.timestamp(data["asOfDate"])

        # TODO: Update these with real values
        computed_balance: ComputedBalance = ComputedBalance()

        account_balance: AccountBalance = AccountBalance(account_id, as_of_date, computed_balance)
        return account_balance


