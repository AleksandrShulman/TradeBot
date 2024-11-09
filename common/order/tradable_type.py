from enum import Enum


class TradableType(Enum):
    Equity = "EQ",
    Option = "OPTN",
    MutualFund = "MF",
    MoneyMarketFund = "MMF"
