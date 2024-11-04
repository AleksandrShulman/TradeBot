import datetime

from common.finance.amount import Amount
from common.finance.currency import Currency
from common.finance.equity import Equity
from common.finance.option import Option
from common.finance.option_style import OptionStyle
from common.finance.option_type import OptionType


ticker = "GE"

type = OptionType.PUT
type2 = OptionType.CALL

strike = Amount(165, 0, Currency.US_DOLLARS)

expiry = datetime.datetime(2025, 3, 21).date()
expiry2 = datetime.datetime.today().date()

price = Amount(0, 87, Currency.US_DOLLARS)
style = OptionStyle.AMERICAN


def get_sample_expiry():
    return expiry


def get_sample_price():
    return price


def get_sample_strike():
    return strike


def get_sample_option():
    return Option(get_sample_equity(), type, strike, expiry, style)


def get_sample_equity():
    return Equity(ticker, "General Electric")
