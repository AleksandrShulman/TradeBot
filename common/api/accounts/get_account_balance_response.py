from common.account.account import Account
from common.account.account_balance import AccountBalance
from common.account.computed_balance import ComputedBalance
from common.account.option_level import OptionLevel
from common.api.response import Response


class GetAccountBalanceResponse(Response):
    def __init__(self, account_balance: AccountBalance):
        self.account_balance: AccountBalance = account_balance

    def __str__(self):
        return f"AccountBalance: {self.account_balance}"