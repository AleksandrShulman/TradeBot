import datetime

from common.finance.amount import Amount
from common.finance.currency import Currency
from common.finance.equity import Equity
from trident.research.calendar_spread_constructor import CalendarSpreadCell

expiry_1 = datetime.datetime(2024, 11, 18).date()
expiry_2 = datetime.datetime(2024, 11, 22).date()

option_delta_atm = (Amount(1, 28, Currency.US_DOLLARS), Amount(1, 58, Currency.US_DOLLARS))
option_delta_otm = Amount(0, 27, Currency.US_DOLLARS), Amount(0, 47, Currency.US_DOLLARS)

class TestCalendarSpreadCell:
    equity = Equity("SPY", "SPDR")

    def test_division(self):
        cell = CalendarSpreadCell(expiry_1, expiry_2, option_delta_atm, option_delta_otm)
        assert cell.get_price_ratio() == round((1.58 - 1.28)/(.47-.27), 3)

    def test_subtraction(self):
        cell = CalendarSpreadCell(expiry_1, expiry_2, option_delta_atm, option_delta_otm)
        assert cell.get_price_difference() == Amount(0, 10, Currency.US_DOLLARS)
        pass