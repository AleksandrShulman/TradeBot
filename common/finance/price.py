from statistics import mean


class Price:
    def __init__(self, bid: float, ask: float, last=None):
        self.bid: float = round(bid, 2)
        self.ask: float = round(ask, 2)
        self.mark: float = round(mean([self.bid, self.ask]), 2)

        if last:
           self.last = round(last, 2)

    def __str__(self):
        self.mark = round(mean([self.bid, self.ask]), 2)
        return f"{self.mark:.2f}\t|\t{self.bid:.2f}\t|\t{self.ask:.2f}\t"

    def copy_of(self):
        if hasattr(self, 'last'):
            return Price(self.bid, self.ask, self.last)
        return Price(self.bid, self.ask)
