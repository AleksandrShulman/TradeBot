import math

from common.finance.currency import Currency


class Amount:
    def __init__(self, whole: int, part: int, currency: Currency = Currency.US_DOLLARS, negative=False):
        self.whole: int = whole
        self.part: int = part
        self.currency: Currency = currency
        self.negative: bool = negative

        if whole < 0 or part < 0:
            raise Exception("Please only include magnitude, for part and whole. Sign set using negative field")
        if part > 99:
            raise Exception("Invalid value for part")

    @staticmethod
    def from_string(input_str: str, currency=Currency.US_DOLLARS):
        if not input_str:
            raise Exception("could not parse input")

        if "." in input_str:
            (whole, part) = input_str.split('.')
            part = part[:2]
        else:
            input_str = input_str.strip("$")
            whole = input_str
            part = 0

        negative = input_str.startswith('-')
        whole = ''.join(c for c in whole if (c.isdigit()))

        return Amount(int(whole), int(part), currency, negative)

    @staticmethod
    def from_float(input_float: float, currency=Currency.US_DOLLARS):
        if input_float is None:
            raise Exception("could not parse input")

        if input_float == 0.0 or input_float == 0:
            return Amount(0,0, currency)

        return Amount.from_string(str(input_float), currency)

    def __add__(self, other):
        if other.currency != self.currency:
            raise Exception("implicit currency conversion not supported")

        total = self.in_smallest_denomination() + other.in_smallest_denomination()

        new_whole: int = math.floor(total / 100)
        new_part: int = total % 100

        return Amount(new_whole, new_part, self.currency)

    def __sub__(self, other):
        if other.currency != self.currency:
            raise Exception("implicit currency conversion not supported")

        total = self.in_smallest_denomination() - other.in_smallest_denomination()

        new_whole: int = math.floor(abs(total) / 100)
        new_part: int = abs(total) % 100

        return Amount(new_whole, new_part, self.currency, total < 0)

    # This is a scalar operation, returning an Amount, as it makes no sense to multiply two amounts together (units would be Currency^2)
    def __mul__(self, other: float):
        total: float = float(abs(self.in_smallest_denomination())) * abs(other)
        negative = self.negative ^ (other < 0)


        new_whole: int = math.floor(total / 100)
        new_part: int = round(total % 100)

        return Amount(new_whole, new_part, self.currency, negative)

    # This can be a scalar operation (units are Currency). It can also be a simple float b/c we'd get a ratio if we divided two values.
    def __truediv__(self, other)->float:
        if other.currency != self.currency:
            raise Exception("implicit currency conversion not supported")

        total: float = float(float(self.in_smallest_denomination()) / float(other.in_smallest_denomination()))
        return round(total, 2)

    def in_smallest_denomination(self) -> int:
        nominal = self.whole * 100 + self.part
        if self.negative:
            return -1 * nominal
        return nominal

    def to_float(self):
        return self.whole + self.part / 100.0

    def __str__(self):
        return f"{self.whole}.{self.part}"

    def __le__(self, other):
        nominal: int = self.whole * 100 + self.part
        nominal_other: int = other.whole * 100 + other.part
        if self.negative:
            nominal = -1 * nominal
        if other.negative:
            nominal_other = -1 * nominal

        return nominal < nominal_other

    def __eq__(self, other):
        if other.currency != self.currency:
            return False

        if other.whole != self.whole:
            return False

        if other.part != self.part:
            return False

        return True

    def __hash__(self):
        # TODO: Figure out a more standard way of hashing
        return hash(str(self.whole) + str(self.part) + str(self.currency))