import datetime

from pandas import DataFrame

from common.exchange.etrade.etrade_connector import ETradeConnector
from common.finance.amount import Amount
from common.finance.chain import Chain
from common.finance.equity import Equity
from common.finance.price import Price
from quotes.api.get_option_expire_dates_request import GetOptionExpireDatesRequest
from quotes.api.get_options_chain_request import GetOptionsChainRequest
from quotes.api.get_options_chain_response import GetOptionsChainResponse
from quotes.api.get_tradable_request import GetTradableRequest
from quotes.etrade.etrade_quote_service import ETradeQuoteService
from quotes.quote_service import QuoteService

from sortedcontainers import SortedDict

DEFAULT_NUM_STRIKES = 15
DEFAULT_DELTA_FROM_CURRENT_PRICE = 5

class CalendarSpreadCell:
    def __init__(self, starting_expiry: datetime.datetime.date, ending_expiry: datetime.datetime.date, starting_strike_value: Amount, ending_strike_value: Amount):
        self.starting_expiry: datetime.datetime.date = starting_expiry
        self.ending_expiry: datetime.datetime.date = ending_expiry
        self.starting_strike_value: Amount = starting_strike_value
        self.ending_strike_value: Amount = ending_strike_value
        self.ratio: float = self.get_price_ratio()
        self.price_difference = self.get_price_difference()

    def get_price_ratio(self) -> float:
        return float(self.ending_strike_value / self.starting_strike_value)

    def get_price_difference(self) -> Amount:
        return self.ending_strike_value - self.starting_strike_value

class CalendarSpreadConstructor:
    def __init__(self, qs: QuoteService, equity: Equity, num_strikes: int = DEFAULT_NUM_STRIKES):
        # The number of strikes into the future
        self.qs:QuoteService = qs
        self.num_strikes: int = num_strikes

        # The security in question
        self.equity: Equity = equity

        self.options_chain: Chain = self.build_options_chain()

    def build_options_chain(self) -> Chain:
        get_option_expire_dates_request = GetOptionExpireDatesRequest(self.equity.ticker)
        option_expire_dates_response = self.qs.get_option_expire_dates(get_option_expire_dates_request)

        options_chain = Chain(self.equity)
        for expiry in option_expire_dates_response.expire_dates[:self.num_strikes]:
            get_options_chain_request: GetOptionsChainRequest = GetOptionsChainRequest(self.equity, expiry)
            get_options_chain_response: GetOptionsChainResponse = self.qs.get_options_chain(get_options_chain_request)
            options_list = get_options_chain_response.options_chain

            print(f"Adding options from {expiry}")
            options_chain.add_chain(options_list)

        return options_chain

    def get_current_price(self)->float:
        return self.qs.get_tradable_quote(GetTradableRequest(self.equity)).current_price.mark

    def build_matrix(self, delta_from_current_price: int=DEFAULT_DELTA_FROM_CURRENT_PRICE)->DataFrame:
        current_price = self.get_current_price()

        # to nearest $.5
        #current_price_to_nearest_dollar: float = round(current_price*2)/2
        current_price_to_nearest_dollar: float = round(current_price)
        print(f"Current price to nearest dollar is: {current_price_to_nearest_dollar}")


        calls = self.options_chain.strike_expiry_chain_call
        puts = self.options_chain.strike_expiry_chain_put

        call_price = Amount.from_float(current_price_to_nearest_dollar + delta_from_current_price)
        put_price = Amount.from_float(current_price_to_nearest_dollar - delta_from_current_price)

        call_chain: dict[datetime, Price] = SortedDict(calls[call_price])
        put_chain: dict[datetime, Price] = SortedDict(puts[put_price])

        call_output: dict[datetime, datetime, CalendarSpreadCell] = dict[datetime, datetime, CalendarSpreadCell]()
        put_output: dict[datetime, datetime, CalendarSpreadCell] = dict[datetime, datetime, CalendarSpreadCell]()

        # Calls
        for calendar_start_index, (calendar_start_date, start_price)  in enumerate(call_chain.items()):
            for calendar_end_index, (calendar_end_date,  end_price) in enumerate(call_chain.items()):
                if calendar_start_date >= calendar_end_date:
                    continue

                cell = CalendarSpreadCell(calendar_start_date, calendar_end_date, Amount.from_float(start_price.mark), Amount.from_float(end_price.mark))
                if calendar_start_date not in call_output:
                    call_output[calendar_start_date] = dict[datetime, CalendarSpreadCell]()
                call_output[calendar_start_date][calendar_end_index] = cell

        # Puts
        for calendar_start_index, (calendar_start_date, start_price) in enumerate(put_chain.items()):
            for calendar_end_index, (calendar_end_date, end_price) in enumerate(put_chain.items()):
                if calendar_start_date >= calendar_end_date:
                    continue

                cell = CalendarSpreadCell(calendar_start_date, calendar_end_date, Amount.from_float(start_price.mark), Amount.from_float(end_price.mark))
                if calendar_start_date not in put_output:
                    put_output[calendar_start_date] = dict[datetime, CalendarSpreadCell]()
                put_output[calendar_start_date][calendar_end_index] = cell

        pass

if __name__ == "__main__":
    connector: ETradeConnector = ETradeConnector()
    q: QuoteService = ETradeQuoteService(connector)

    ticker = "SPY"
    equity_name = "SPDR S&P 500 ETF TRUST"

    equity: Equity = Equity(ticker, equity_name)
    constructor = CalendarSpreadConstructor(q, equity, 4)
    constructor.build_matrix()