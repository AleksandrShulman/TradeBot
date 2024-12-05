import logging
from datetime import datetime

from common.account.computed_balance import ComputedBalance
from common.account.option_level import OptionLevel

logger = logging.getLogger(__name__)


class AccountBalance:
    def __init__(self, account_id: str, as_of_date: datetime, computed_balance: ComputedBalance):
        self.account_id = account_id
        self.as_of_date: datetime = as_of_date
        self.computed_balance: ComputedBalance = computed_balance

    def __str__(self):
        return f"{' - '.join([self.__getattribute__(x) for x in self.__dict__ if self.__getattribute__(x)])}"

    def __repr__(self):
        return self.__str__()