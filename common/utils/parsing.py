from common.finance.equity import Equity
from common.finance.option import Option
from common.finance.price import Price
from common.portfolio.portfolio import Portfolio
from common.utils.local_ticker_lookup import LocalTickerLookup


def parse_into_portfolio(dataframe) -> Portfolio:
    portfolio = Portfolio()
    for row in dataframe:
        symbol: str = row["Symbol"]
        quantity = row["Qty #"]
        split = symbol.split(" ")
        price = parse_price_from_row(row)

        if len(split) == 1:
            ticker = split[0]
            tradable = Equity(ticker, LocalTickerLookup.lookup(ticker))
        else:
            tradable = Option.from_str(" ".join(split))

        tradable.set_price(price)
        portfolio.add_position(tradable, quantity)

    return portfolio


def parse_price_from_row(row):
    bid = float(row["Bid"])
    ask = float(row["Ask"])
    return Price(bid, ask)
