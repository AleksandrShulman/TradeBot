from datetime import datetime

from common.api.request import Request
from common.order.order_status import OrderStatus


DEFAULT_ORDER_LIST_COUNT = 200


class OrderListRequest(Request):
    def __init__(self, account_id: str, status: OrderStatus, from_date: datetime.date,
                    to_date: datetime.date, max_count, exchange_specific_opts: dict[str, str]):
        self.account_id = account_id
        self.status = status
        self.from_date = from_date
        self.to_date = to_date
        self.count = max_count
        self.exchange_specific_opts = exchange_specific_opts