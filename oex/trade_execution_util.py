from pygments import highlight

from common.finance.amount import Amount
from common.finance.price import Price
from common.order.action import Action
from common.order.order import Order
from quotes.api.get_tradable_request import GetTradableRequest
from quotes.api.get_tradable_response import GetTradableResponse
from quotes.quote_service import QuoteService

ADJUSTED_NO_BIDS_WIDE_SPREAD_ASK = .03

class TradeExecutionUtil:
    # This can also be done via order Bid-Ask - advantage is fewer API calls. Downside is relying on ETrade's order service
    # This would be necessary to establish a first price for the order. Other issue is it wouldn't adjust for very wide spreads
    def get_market_price(order: Order, quote_service: QuoteService, adjust_excessive_spreads=True) -> Price:
        mark_to_market_price: float = 0
        best_value: float = 0
        worst_value: float = 0

        for order_line in order.order_lines:
            get_tradable_request: GetTradableRequest = GetTradableRequest(order_line.tradable)
            get_tradable_response: GetTradableResponse = quote_service.get_tradable_quote(get_tradable_request)
            quantity = order_line.quantity

            current_price = get_tradable_response.current_price

            if adjust_excessive_spreads and get_tradable_response.current_price.bid == 0 and get_tradable_response.current_price.ask > .04:
                current_price.ask = ADJUSTED_NO_BIDS_WIDE_SPREAD_ASK

            if Action.is_long(order_line.action):
                worst_value -= current_price.bid * quantity
                best_value -= current_price.ask * quantity

                mark_to_market_price -= get_tradable_response.current_price.mark
            else:
                worst_value += current_price.ask * quantity
                best_value += current_price.bid * quantity

                mark_to_market_price += get_tradable_response.current_price.mark

        # This is not obvious and quite surprising. In cases where there's a credit, bid is the lower credit, ask is the higher credit.
        # Where there is at least one debit, the higher price is the bid and the lower is the ask
        if best_value >= 0 and worst_value >= 0:
            lower = best_value
            upper = worst_value
        else:
            lower = max(best_value, worst_value)
            upper = min(best_value, worst_value)

        return Price(lower, upper)