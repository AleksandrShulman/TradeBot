from datetime import datetime

import pytest as pytest

from common.finance.amount import Amount
from common.finance.currency import Currency
from common.finance.equity import Equity
from common.finance.option import Option
from common.finance.option_style import OptionStyle
from common.finance.option_type import OptionType
from common.order.expiry.good_for_day import GoodForDay
from common.order.expiry.good_for_sixty_days import GoodForSixtyDays

e = Equity("GE", "General Electric")
type = OptionType.PUT
type2 = OptionType.CALL

strike = Amount(10, 0, Currency.US_DOLLARS)

expiry = GoodForSixtyDays().expiry_date
expiry2 = GoodForDay().expiry_date

price = Amount(0, 87, Currency.US_DOLLARS)
style = OptionStyle.AMERICAN


def test_option_construction():
    o: Option = Option(e, type, strike, expiry, style)
    assert o.expiry is expiry


def test_option_empty_type():
    with pytest.raises(Exception, match='Missing var!'):
        Option(e, None, strike, expiry, style)


def test_option_none_date():
    with pytest.raises(Exception, match='Missing var!'):
        Option(e, type, strike, None, style)


def test_option_equality():
    o: Option = Option(e, type, strike, expiry, style)
    o2: Option = Option(e, type, strike, expiry, style)

    assert o == o2


def test_option_inequality_type():
    o: Option = Option(e, type, strike, expiry, style)
    o2: Option = Option(e, type2, strike, expiry, style)

    assert o != o2


def test_option_inequality_expiry():
    o: Option = Option(e, type, strike, expiry, style)
    o2: Option = Option(e, type, strike, expiry2, style)

    assert o != o2


def test_option_parsing_european():
    input_str = "VIX Oct 16 '24 $19 Call"
    o = Option.from_str(input_str)

    assert o.type == OptionType.CALL
    assert o.strike == Amount(19, 0)
    assert datetime(2024, 10, 16) == o.expiry
    assert o.style == OptionStyle.EUROPEAN


def test_option_parsing_american():
    input_str = "RIOT Nov 08 '24 $7.50 Call"
    o = Option.from_str(input_str)

    assert o.type == OptionType.CALL
    assert o.strike == Amount(7, 50)
    assert datetime(2024, 11, 8) == o.expiry
    assert o.style == OptionStyle.AMERICAN

