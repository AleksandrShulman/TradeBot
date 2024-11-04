import pytest as pytest

from common.finance.equity import Equity


def test_equity_string():
    e = Equity("GE", "General Electric")
    assert e.__str__() == "GE: General Electric"


def test_equity_empty_ticker():
    with pytest.raises(Exception, match='not valid'):
        Equity("", "General Electric")


def test_equity_none_name():
    with pytest.raises(Exception, match='not valid'):
        Equity("GE", None)
