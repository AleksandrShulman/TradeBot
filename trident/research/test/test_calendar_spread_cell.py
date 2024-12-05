import datetime

from common.finance.amount import Amount
from common.finance.currency import Currency
from common.finance.equity import Equity
from trident.research.calendar_spread_constructor import CalendarSpreadCell

expiry_1 = datetime.datetime(2024, 11, 18).date()
expiry_2 = datetime.datetime(2024, 11, 22).date()

option_delta_at_expiry_1 = Amount(0, 28, Currency.US_DOLLARS)
option_delta_at_expiry_2 = Amount(0, 77, Currency.US_DOLLARS)

class TestCalendarSpreadCell:
    equity = Equity("SPY", "SPDR")

    def test_division(self):
        cell = CalendarSpreadCell(expiry_1, expiry_2, option_delta_at_expiry_1, option_delta_at_expiry_2)
        assert cell.get_price_ratio() == round(77/28,2)

    def test_subtraction(self):
        cell = CalendarSpreadCell(expiry_1, expiry_2, option_delta_at_expiry_1, option_delta_at_expiry_2)
        assert cell.get_price_difference() == Amount(0, 49, Currency.US_DOLLARS)
        pass