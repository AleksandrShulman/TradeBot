from common.finance.equity import Equity
from common.finance.option_type import OptionType
from common.finance.options.option_order import OptionOrder
from common.finance.options.option_order_line import OptionOrderLine
from common.finance.options.spread import Spread
from common.order.action import Action
from common.order.order_price import OrderPrice
from common.order.order_type import OrderType


class Condor(OptionOrder):
    def __init__(self, order_price: OrderPrice, options: list[OptionOrderLine]):

        if type(Equity) in [type(option.tradable) for option in options]:
            raise Exception()

        if len(options) != 4:
            raise Exception(f"Should have 4 legs. {len(options)} provided")

        puts = [option_order_line for option_order_line in options if option_order_line.tradable.type == OptionType.PUT]
        calls = [option_order_line for option_order_line in options if option_order_line.tradable.type == OptionType.CALL]

        if puts and calls:
            raise Exception(f"Should only have one type in a Condor. There are {len(puts)} and {len(calls)} calls.")

        super().__init__(order_price, options)

        shorts = [option_order_line for option_order_line in options if not Action.is_long(option_order_line.action)]
        longs = [option_order_line for option_order_line in options if Action.is_long(option_order_line.action)]

        sorted_shorts = sorted(shorts, key=lambda x: x.tradable.strike)
        sorted_longs = sorted(longs, key=lambda x: x.tradable.strike)

        # Need higher short/long pair
        self.spread_1_order_lines = [sorted_shorts[0], sorted_longs[0]]
        self.spread_2_order_lines = [sorted_shorts[1], sorted_longs[1]]


    def get_order_type(self) -> OrderType:
        return OrderType.CONDOR


    def _organize_into_order_lines(self):
        shorts = [option_order_line for option_order_line in self.options if not Action.is_long(option_order_line.action)]
        longs = [option_order_line for option_order_line in self.options if Action.is_long(option_order_line.action)]

        sorted_shorts = sorted(shorts, key=lambda x: x.tradable.strike)
        sorted_longs = sorted(longs, key=lambda x: x.tradable.strike)

        # Need higher short/long pair
        self.spread_1_order_lines = [sorted_shorts[0], sorted_longs[0]]
        self.spread_2_order_lines = [sorted_shorts[1], sorted_longs[1]]