from datetime import datetime, timedelta

from common.finance.amount import Amount
from common.finance.price import Price
from common.order.order_price_type import OrderPriceType
from common.order.placed_order import PlacedOrder
from tex.scripts.trade_until_executed import DEFAULT_WAIT
from tex.tactics.execution_tactic import ExecutionTactic

GAP_REDUCTION_RATIO = 1/3
DEFAULT_WAIT = timedelta(seconds=15)

class IncrementalPriceDeltaExecutionTactic(ExecutionTactic):
    @staticmethod
    def new_price(placed_order: PlacedOrder)->Amount:
        current_market_price: Price = placed_order.placed_order_details.current_market_price
        current_market_mark_to_market_price = current_market_price.mark
        current_order_price: float = placed_order.order.order_price.price.to_float()

        delta = current_order_price - current_market_mark_to_market_price
        order_price_type = placed_order.order.order_price.order_price_type
        if delta > 0:
            # For equity orders, this kind of does not make sense
            if order_price_type in [OrderPriceType.NET_CREDIT, OrderPriceType.LIMIT]:
                # decrease the price
                new_delta = delta * (1-GAP_REDUCTION_RATIO)
                adjustment = delta - new_delta
                return Amount.from_float(current_order_price - adjustment)
            else:
                # this means that we're actually buying over the current market price, and it represents a stuck market
                pass
        else:
            if order_price_type in [OrderPriceType.NET_DEBIT, OrderPriceType.LIMIT]:
                new_delta = delta * (1 - GAP_REDUCTION_RATIO)
                adjustment = delta - new_delta
                return Amount.from_float(current_order_price - adjustment)
            else:
                # this means that we're actually selling under the current market price, and it represents a stuck market
                pass
        # Should have a better default return value
        return Amount(0,0)