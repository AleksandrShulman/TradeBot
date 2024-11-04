import logging
from datetime import datetime

from common.exchange.etrade.etrade_connector import ETradeConnector
from common.finance.equity import Equity
from common.finance.option import Option
from common.finance.price import Price
from common.finance.tradable import Tradable
from quotes.api.tradable_request import TradableRequest
from quotes.api.tradable_response import TradableResponse
from quotes.quote_service import QuoteService


# The ETrade API allows for mixed requests for both options and equities. There are a host of other
# Exchange-specific request configurations


"""
Property	Type	Required?	Description	Allowable Values
symbols	path	yes	One or more (comma-separated) symbols for equities or options, up to a maximum of 25. Symbols for equities are simple, for example, GOOG. Symbols for options are more complex, consisting of six elements separated by colons, in this format: underlier:year:month:day:optionType:strikePrice.	
detailFlag	query	no	Determines the market fields returned from a quote request.	ALL, FUNDAMENTAL, INTRADAY, OPTIONS, WEEK_52, MF_DETAIL
requireEarningsDate	query	no	If value is true, then nextEarningDate will be provided in the output. If value is false or if the field is not passed, nextEarningDate will be returned with no value.	
overrideSymbolCount	query	no	If value is true, then symbolList may contain a maximum of 50 symbols; otherwise, symbolList can only contain 25 symbols.	
skipMiniOptionsCheck	query	no	If value is true, no call is made to the service to check whether the symbol has mini options. If value is false or if the field is not specified, a service call is made to check if the symbol has mini options.
"""

logger = logging.getLogger(__name__)


class ETradeQuoteService(QuoteService):

    def get_tradable_quote(self, tradable_request: TradableRequest) -> TradableResponse:

        connector: ETradeConnector = self.connector
        session, base_url = connector.load_connection()

        tradable = tradable_request.get_tradable()
        if isinstance(tradable, Option):
            # format is: underlying:year:month:day:optionType:strikePrice.
            as_option: Option = tradable
            ticker = as_option.equity.ticker
            expiry = as_option.expiry
            strike = as_option.strike
            type = as_option.type
            symbols = f"{ticker}:{expiry.year}:{expiry.month}:{expiry.day}:{type}:{strike}"
        elif isinstance(tradable, Equity):
            as_option: Equity = tradable
            symbols = as_option.ticker
        else:
            raise Exception(f"Tradable type {type(tradable)} not recognized")

        path = f"/v1/market/quote/{symbols}.json"
        url = base_url + path
        response = session.get(url)
        tradable_response = ETradeQuoteService._parse_market_response(tradable, response)

        return tradable_response

    def get_equity_quote(self, symbol: str):

        pass

    def get_options_chain_for_expiry(self, symbol: str, expiry: datetime):
        pass

    def get_option_details(self, option: Option):
        pass

    @staticmethod
    def _parse_market_response(tradable: Tradable, input):
        data: dict = input.json()
        if data is not None and "QuoteResponse" in data and "QuoteData" in data["QuoteResponse"]:
            for quote in data["QuoteResponse"]["QuoteData"]:
                if quote is not None and "dateTime" in quote:
                    print("Date Time: " + quote["dateTime"])
                response_time = quote["dateTime"]
                if quote is not None and "All" in quote and "lastTrade" in quote["All"]:
                    if quote is not None and "All" in quote and "bid" in quote["All"] and "bidSize" in quote["All"]:
                        print("Bid (Size): " + str('{:,.2f}'.format(quote["All"]["bid"])) + "x" + str(
                            quote["All"]["bidSize"]))
                        bid = quote["All"]["bid"]
                    if quote is not None and "All" in quote and "ask" in quote["All"] and "askSize" in quote["All"]:
                        print("Ask (Size): " + str('{:,.2f}'.format(quote["All"]["ask"])) + "x" + str(
                            quote["All"]["askSize"]))
                        ask = quote["All"]["ask"]
                    if quote is not None and "All" in quote and "totalVolume" in quote["All"]:
                        print("Volume: " + str('{:,}'.format(quote["All"]["totalVolume"])))
                        volume = quote["All"]["totalVolume"]
                return TradableResponse(tradable, response_time, Price(bid, ask), volume)
            else:
                # Handle errors
                if data is not None and 'QuoteResponse' in data and 'Messages' in data["QuoteResponse"] \
                        and 'Message' in data["QuoteResponse"]["Messages"] \
                        and data["QuoteResponse"]["Messages"]["Message"] is not None:
                    for error_message in data["QuoteResponse"]["Messages"]["Message"]:
                        print("Error: " + error_message["description"])
                else:
                    print("Error: Quote API service error")
        else:
            logger.debug("Response Body: %s", input)
            print("Error: Quote API service error")
