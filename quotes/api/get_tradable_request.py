from pydantic import BaseModel

from common.finance.tradable import Tradable
from common.api.request import Request


class GetTradableRequest(Request, BaseModel):
    tradable: Tradable

    def get_tradable(self):
        return self.tradable

    def __eq__(self, other):
        if other.tradable != self.tradable:
            return False
        return True