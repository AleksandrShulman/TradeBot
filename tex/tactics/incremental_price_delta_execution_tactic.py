from datetime import timedelta

from common.api.test.orders.order_test_util import DEFAULT_AMOUNT
from common.finance.amount import Amount
from common.finance.price import Price
from common.order.order_price_type import OrderPriceType
from common.order.placed_order import PlacedOrder
from quotes.quote_service import QuoteService
from tex.tactics.execution_tactic import ExecutionTactic
from tex.trade_execution_util import TradeExecutionUtil

GAP_REDUCTION_RATIO = 1/3
DEFAULT_WAIT_SEC = 4
VERY_CLOSE_TO_MARKET_PRICE_WAIT = 30

class IncrementalPriceDeltaExecutionTactic(ExecutionTactic):
    @staticmethod
    def new_price(placed_order: PlacedOrder, quote_service: QuoteService=None)->(Amount, int):
        current_market_price: Price = placed_order.placed_order_details.current_market_price
        current_market_mark_to_market_price: float = current_market_price.mark
        current_order_price: float = placed_order.order.order_price.price.to_float()

        if not current_market_mark_to_market_price and quote_service:
            # After-hours it doesn't seem to provide this data in the E*Trade response. No matter, we can pull it from the exchange
            current_market_mark_to_market_price = TradeExecutionUtil.get_market_price(placed_order.order, quote_service).to_float()

        delta = current_order_price - current_market_mark_to_market_price
        order_price_type = placed_order.order.order_price.order_price_type
        if delta > 0:
            # For equity orders, this kind of does not make sense
            if order_price_type in [OrderPriceType.NET_CREDIT, OrderPriceType.LIMIT]:
                # decrease the price
                new_delta = delta * (1-GAP_REDUCTION_RATIO)
                adjustment = max(delta - new_delta, .01)
                return Amount.from_float(round(current_order_price - adjustment,2)), DEFAULT_WAIT_SEC
            else:
                # this means that we're actually buying over the current market price, and it represents a stuck market
                pass
        else:
            if order_price_type in [OrderPriceType.NET_DEBIT, OrderPriceType.LIMIT]:
                new_delta = delta * (1 - GAP_REDUCTION_RATIO)

                adjustment = min(delta-new_delta, -0.01)
                wait_time = DEFAULT_WAIT_SEC

                return Amount.from_float(round(current_order_price - adjustment,2)), wait_time
            else:
                # this means that we're actually selling under the current market price, and it represents a stuck market
                pass
        # Should have a better default return value
        return Amount(0,0), DEFAULT_WAIT_SEC