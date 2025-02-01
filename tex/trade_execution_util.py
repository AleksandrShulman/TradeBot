from common.finance.amount import Amount
from common.order.action import Action
from common.order.order import Order
from quotes.api.get_tradable_request import GetTradableRequest
from quotes.api.get_tradable_response import GetTradableResponse
from quotes.quote_service import QuoteService

DEFAULT_NO_BIDS_PRICE = Amount(0, 2)

class TradeExecutionUtil:
    # This can also be done via a Bid-Ask - advantage is fewer API calls. Downside is relying on ETrade's order service
    # This would be necessary to establish a first price for the order
    def get_market_price(order: Order, quote_service: QuoteService) -> Amount:
        mark_to_market_price: float = 0
        for order_line in order.order_lines:
            get_tradable_request: GetTradableRequest = GetTradableRequest(order_line.tradable)
            get_tradable_response: GetTradableResponse = quote_service.get_tradable_quote(get_tradable_request)
            if get_tradable_response.current_price.bid == 0:
                # sometimes for thinly traded, far OTM options, the spreads are quite wide.
                # if the delta is >= $.10, we can just mark it as "$.02", since it takes at least $.01 to buy, and
                # these are often thinly traded, so we'll have to add a bit more.
                mark_to_market_price += DEFAULT_NO_BIDS_PRICE
            elif Action.is_long(order_line.action):
                mark_to_market_price += get_tradable_response.current_price.mark
            else:
                mark_to_market_price -= get_tradable_response.current_price.mark

        return Amount.from_float(mark_to_market_price)
