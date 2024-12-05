from statistics import mean


class Price:
    def __init__(self, bid, ask, last=None):
        self.bid = round(bid, 2)
        self.ask = round(ask, 2)
        self.mark = round(mean([self.bid, self.ask]), 2)

        if last:
           self.last = round(last, 2)

    def __str__(self):
        self.mark = round(mean([self.bid, self.ask]), 2)
        return f"{self.mark:.2f}\t|\t{self.bid:.2f}\t|\t{self.ask:.2f}\t"

    def copy_of(self):
        return Price(self.bid, self.ask, self.last)
