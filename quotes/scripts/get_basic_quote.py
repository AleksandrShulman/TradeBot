from common.exchange.etrade.etrade_connector import ETradeConnector
from common.finance.equity import Equity
from common.finance.option import Option
from common.test.util.test_object_util import get_sample_equity, get_sample_option
from quotes.api.tradable_request import TradableRequest
from quotes.api.tradable_response import TradableResponse
from quotes.etrade.etrade_quote_service import ETradeQuoteService
from quotes.quote_service import QuoteService

if __name__ == "__main__":
    connector: ETradeConnector = ETradeConnector()

    equity: Equity = get_sample_equity()
    option: Option = get_sample_option()
    equity_request: TradableRequest = TradableRequest(equity)
    option_request: TradableRequest = TradableRequest(option)

    q: QuoteService = ETradeQuoteService(connector)
    equity_response: TradableResponse = q.get_tradable_quote(equity_request)

    option_response: TradableResponse = q.get_tradable_quote(option_request)

    print(option_response)