from datetime import datetime


from common.finance.amount import Amount
from common.finance.equity import Equity
from common.finance.exercise_style import ExerciseStyle
from common.finance.option_type import OptionType
from common.finance.tradable import Tradable
from common.utils.local_ticker_lookup import LocalTickerLookup

from dateutil.parser import parse


class Option(Tradable):
    def __init__(self, equity: Equity, type: OptionType,
                 strike: Amount, expiry: datetime.date, style: ExerciseStyle):
        self.equity: Equity = equity
        self.type: OptionType = type
        self.strike: Amount = strike
        self.expiry: datetime.date = expiry
        self.style: ExerciseStyle = style

        for var in vars(self):
            if self.__getattribute__(var) is None:
                raise Exception(f"Missing var! - {var}")

    def copy_of(self):
        return Option(self.equity, self.type, self.strike, self.expiry, self.style)

    def __eq__(self, other):
        if not type(other) == type(self):
            raise Exception(f"Cannot compare option to non-option: {self.type}")

        if self.equity != other.equity:
            return False

        if self.type != other.type:
            return False

        if self.strike != other.strike:
            return False

        if self.expiry != other.expiry:
            return False

        if self.style != other.style:
            return False

        return True

    @staticmethod
    # Space-delimited info in the form $TICKET MM DD YY $STRIKE TYPE
    def from_str(input: str):
        components = input.split(' ')
        ticker: int = components[0]
        expiry: datetime = parse(" ".join(components[1:4]))
        strike: Amount = Amount.from_string(components[4])
        type: OptionType = OptionType.from_str(components[5])

        company_name = LocalTickerLookup.lookup(ticker)

        return Option(Equity(ticker, company_name), type, strike, expiry, ExerciseStyle.from_ticker(ticker))