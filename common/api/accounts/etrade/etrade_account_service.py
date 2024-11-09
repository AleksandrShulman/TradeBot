from common.account.account import Account
from common.api.accounts.account_list_response import AccountListResponse
from common.api.accounts.account_service import AccountService
from common.api.accounts.get_account_info_request import GetAccountInfoRequest
from common.api.accounts.get_account_info_response import GetAccountInfoResponse
from common.exchange.etrade.etrade_connector import ETradeConnector


class ETradeAccountService(AccountService):

    def __init__(self, connector: ETradeConnector):
        super().__init__(connector)
        self.session, self.base_url = self.connector.load_connection()

    def list_accounts(self) -> AccountListResponse:
        path = f"/v1/accounts/list.json"
        url = self.base_url + path
        response = self.session.get(url)
        account_list_response = ETradeAccountService._parse_account_list_response(response)
        return account_list_response

    def get_account_info(self, get_account_info_request: GetAccountInfoRequest) -> GetAccountInfoResponse:
        path = f"/v1/accounts/list.json"
        url = self.base_url + path
        response = self.session.get(url)

        name_filter = (lambda a: a.account_id == get_account_info_request.account_id)

        account_list_response: AccountListResponse = ETradeAccountService._parse_account_list_response(response, name_filter)
        if len(account_list_response.get_account_list()) > 1:
            raise Exception("More than one result")

        if len(account_list_response.get_account_list()) == 1:
            return GetAccountInfoResponse(account_list_response.get_account_list()[0])

        return GetAccountInfoResponse(None)

    @staticmethod
    def _parse_account_list_response(input, f=(lambda a: a)) -> list[Account]:
        data: dict = input.json()
        if 'error' in data:
            code = data['error']['code']
            message = data['error']['message']
            raise Exception(f"Error from E*Trade: {code}: {message}")
        account_list_response = data["AccountListResponse"]
        accounts: list[Account] = account_list_response["Accounts"]

        return_accounts = map(lambda account: Account(account["accountId"],
                                                    account["accountName"], account["accountDesc"]), accounts["Account"])

        return AccountListResponse(list(filter(f, return_accounts)))


