import datetime
import json

from common.api.portfolio.GetPortfolioRequest import GetPortfolioRequest
from common.api.portfolio.GetPortfolioResponse import GetPortfolioResponse
from common.api.portfolio.portfolio_service import PortfolioService
from common.exchange.connector import Connector
from common.finance.amount import Amount
from common.finance.equity import Equity
from common.finance.option import Option
from common.finance.option_style import OptionStyle
from common.finance.option_type import OptionType
from common.finance.tradable import Tradable
from common.portfolio.portfolio import Portfolio

DEFAULT_SORT_BY = "DAYS_EXPIRATION"
DEFAULT_SORT_ORDER = "ASC"

DEFAULT_VIEW = "COMPLETE"

DEFAULT_NUM_POSITIONS = 1000

DEFAULT_PORTFOLIO_OPTIONS = {
    "sortBy": DEFAULT_SORT_BY,
    "sortOrder": DEFAULT_SORT_ORDER,
    "view": DEFAULT_VIEW,
    "count": str(DEFAULT_NUM_POSITIONS)
}


class ETradePortfolioService(PortfolioService):
    def __init__(self, connector: Connector):
        super().__init__(connector)
        self.session, self.base_url = self.connector.load_connection()

    def get_portfolio_info(self, get_portfolio_request: GetPortfolioRequest, exchange_specific_options: dict[str, str] = DEFAULT_PORTFOLIO_OPTIONS) -> GetPortfolioResponse:
        account_id = get_portfolio_request.account_id
        count = get_portfolio_request.count

        path = f"/v1/accounts/{account_id}/portfolio.json?"

        if exchange_specific_options:
            options_str = ",".join(f"{k}={v}" for k,v in options.items())
        else:
            options_str = f"count={DEFAULT_NUM_POSITIONS}"

        path += f"?{options_str}"

        url = self.base_url + path
        response = self.session.get(url)
        portfolio_list_response = ETradePortfolioService._parse_portfolio_response(response)
        return portfolio_list_response

    @staticmethod
    def _parse_portfolio_response(input) -> GetPortfolioResponse:
        if input.status_code != 200:
            text = json.loads(input.text)
            error = text['Error']
            message = error['message']
            status_code = input.status_code
            raise Exception(f"Status {status_code}, {message}")
        data: dict = json.load(input)
        portfolio_response = data["PortfolioResponse"]
        account_portfolios = portfolio_response["accountPortfolio"]

        return_portfolio = Portfolio()
        for account_portfolio in account_portfolios:
            positions = account_portfolio["position"]

            for position in positions:
                tradable = ETradePortfolioService._get_tradable_from_position(position)
                quantity = position["quantity"]
                return_portfolio.add_position(tradable, quantity)

        GetPortfolioResponse(return_portfolio)

    @staticmethod
    def _get_tradable_from_position(position) -> Tradable:
        product = position["product"]
        symbol = product["symbol"]
        symbol_desc = position["symbolDesc"]

        e = Equity(symbol, symbol_desc)

        if product["securityType"] == "EQ":
            return e
        elif product["securityType"] == "OPTN":
            option_type: OptionType = OptionType.from_str(product["callPut"])
            strike_price: Amount = Amount.from_string(product["strikePrice"])
            option_style: OptionStyle = OptionStyle.from_expiry_type(product["expiryType"])
            expiry_year: int = product["expiryYear"]
            expiry_day: int = product["expiryDay"]
            expiry_month: int = product["expiryMonth"]
            return Option(e, option_type, strike_price, datetime.datetime(expiry_year, expiry_month, expiry_day).date(), option_style)
        else:
            raise Exception(f"Style {product['securityType']} not supported yet")


