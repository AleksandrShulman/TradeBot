import datetime

from common.exchange.etrade.etrade_connector import ETradeConnector
from common.finance.amount import Amount
from common.finance.chain import Chain
from common.finance.currency import Currency
from common.finance.equity import Equity
from quotes.api.get_option_expire_dates_request import GetOptionExpireDatesRequest
from quotes.api.get_option_expire_dates_response import GetOptionExpireDatesResponse
from quotes.api.get_options_chain_request import GetOptionsChainRequest
from quotes.etrade.etrade_quote_service import ETradeQuoteService
from quotes.quote_service import QuoteService

DEFAULT_NUM_STRIKES = 20


class CalendarSpreadCell:
    def __init__(self, starting_expiry: datetime.datetime.date, ending_expiry: datetime.datetime.date, starting_strike_value: Amount, ending_strike_value: Amount):
        self.starting_expiry: datetime.datetime.date = starting_expiry
        self.ending_expiry: datetime.datetime.date = ending_expiry
        self.starting_strike_value: Amount = starting_strike_value
        self.ending_strike_value: Amount = ending_strike_value

    def get_price_ratio(self)->float:
        return float(self.ending_strike_value / self.starting_strike_value)

    def get_price_difference(self):
        return self.ending_strike_value - self.starting_strike_value

class CalendarSpreadConstructor:
    def __init__(self, qs: QuoteService, equity: Equity, strike_delta: Amount, num_strikes: int = DEFAULT_NUM_STRIKES, ):
        # The number of strikes into the future
        self.qs:QuoteService = qs
        self.num_strikes: int = num_strikes

        # The security in question
        self.equity: Equity = equity

        # Which strikes to pick. This gives an approx dollar range to go up and down from the current price
        self.strike_delta: Amount = strike_delta

    def get_expiry_dates(self) -> list[datetime.date]:
        expiry_dates_request = GetOptionExpireDatesRequest(self.equity.ticker)
        response: GetOptionExpireDatesResponse = self.qs.get_option_expire_dates(expiry_dates_request)
        return response.expire_dates[:self.num_strikes]

    def construct(self):
        #expiries = self.get_expiry_dates()
        expiries = [datetime.date(2024, 12,9), datetime.date(2024, 12,10), datetime.date(2024, 12,11)]
        for expiry in expiries:
            expiry_request = GetOptionsChainRequest(self.equity, expiry)
            options_chain: Chain = self.qs.get_options_chain(expiry_request)
            print(options_chain)
            pass

if __name__ == "__main__":
    connector: ETradeConnector = ETradeConnector()
    q: QuoteService = ETradeQuoteService(connector)

    ticker = "SPY"
    equity_name = "SPDR S&P 500 ETF TRUST"


    ticker2 = "GOOG"
    equity_name2 = "SPDR S&P 500 ETF TRUST"


    equity: Equity = Equity(ticker, equity_name)
    equity2: Equity = Equity(ticker2, equity_name2)

    constructor = CalendarSpreadConstructor(q, equity2, Amount(15,0, Currency.US_DOLLARS))
    constructor.construct()