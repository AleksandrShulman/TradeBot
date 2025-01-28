import datetime
from abc import ABC

from common.finance.price import Price
from common.order.placed_order import PlacedOrder


class ExecutionTactic(ABC):
    def new_price_and_order_placement_time(order: PlacedOrder)->(Price, datetime.datetime):
        pass
