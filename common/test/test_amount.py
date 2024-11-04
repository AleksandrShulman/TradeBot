from common.finance.amount import Amount
from common.finance.currency import Currency


def test_add_two_amounts():
    a1 = Amount(10, 15, Currency.US_DOLLARS)
    a2 = Amount(2, 95, Currency.US_DOLLARS)

    a3 = a1 + a2

    assert a3.whole == 13
    assert a3.part == 10
    assert a3.currency == Currency.US_DOLLARS
    assert not a3.negative


def test_subtract_two_amounts():
    a1 = Amount(10, 15, Currency.US_DOLLARS)
    a2 = Amount(2, 95, Currency.US_DOLLARS)

    a3 = a1 - a2

    assert a3.whole == 7
    assert a3.part == 20
    assert a3.currency == Currency.US_DOLLARS
    assert not a3.negative


def test_equals():
    pass


def test_subtract_two_amounts_negative_result():
    a1 = Amount(10, 15, Currency.US_DOLLARS)
    a2 = Amount(2, 95, Currency.US_DOLLARS)

    a3 = a2 - a1

    assert a3.whole == 7
    assert a3.part == 20
    assert a3.currency == Currency.US_DOLLARS
    assert a3.negative


def test_multiply_two_amounts():
    a1 = Amount(10, 15, Currency.US_DOLLARS)
    a2 = Amount(2, 95, Currency.US_DOLLARS)

    a3 = a2 * a1

    assert a3.whole == 29
    assert a3.part == 94
    assert a3.currency == Currency.US_DOLLARS
    print(a3.negative)
    assert False is a3.negative


def test_multiply_two_amounts_is_negative():
    a1 = Amount(10, 15, Currency.US_DOLLARS)
    a2 = Amount(2, 95, Currency.US_DOLLARS, negative=True)

    a3 = a2 * a1

    assert a3.whole == 29
    assert a3.part == 94
    assert a3.currency == Currency.US_DOLLARS
    print(a3.negative)
    assert True is a3.negative