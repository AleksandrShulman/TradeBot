from statistics import mean
from typing import Any, Annotated, Optional

from pydantic import BaseModel, computed_field, field_validator


class Price(BaseModel):
    bid: float
    ask: float
    last: Optional[float] = None

    @field_validator('bid', 'ask', mode='before')
    @classmethod
    def round_to_two_decimals(cls, value: float) -> float:
        return round(value, 2)

    def set_mark(self):
        return (self.bid + self.ask)/2

    @computed_field
    @property
    def set_mark(self)->float:
        return round(mean([self.bid, self.ask]), 2)


    # can be a validator
    if last:
        self.last = round(last, 2)



    def __repr__(self):
        self.mark = round(mean([self.bid, self.ask]), 2) if not self.mark else self.mark
        return f"{self.mark:.2f}\t|\t{self.bid:.2f}\t|\t{self.ask:.2f}\t"

    def __str__(self):
        self.mark = round(mean([self.bid, self.ask]), 2) if not self.mark else self.mark
        return f"{self.mark:.2f}\t|\t{self.bid:.2f}\t|\t{self.ask:.2f}\t"

    def copy_of(self):
        if hasattr(self, 'last'):
            return Price(self.bid, self.ask, self.last)
        return Price(self.bid, self.ask)
