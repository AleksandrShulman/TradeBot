from common.finance.options.equity_order_line import EquityOrderLine
from common.finance.options.option_order import OptionOrder
from common.finance.options.option_order_line import OptionOrderLine
from common.order.order_price import OrderPrice


class BuyWrite(OptionOrder):
    def __init__(self, order_price: OrderPrice, equity: EquityOrderLine, options: list[OptionOrderLine]):
        if len(options) != 1:
            raise Exception("Buy-writes should only have one option leg")
        self.equity = equity
        super().__init__(order_price, options)
