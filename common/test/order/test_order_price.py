from common.finance.amount import ZERO, Amount
from common.order.order_price import OrderPrice
from common.order.order_price_type import OrderPriceType


class TestOrderPrice:
    def test_limit_0_equals_even(self):
        assert OrderPrice(OrderPriceType.NET_EVEN) == OrderPrice(OrderPriceType.NET_CREDIT, ZERO)
        assert OrderPrice(OrderPriceType.NET_EVEN) == OrderPrice(OrderPriceType.NET_DEBIT, ZERO)

    def test_equality(self):
        assert OrderPrice(OrderPriceType.NET_CREDIT, Amount(1,23)) == OrderPrice(OrderPriceType.NET_CREDIT, Amount(1,23))
        assert OrderPrice(OrderPriceType.NET_DEBIT, Amount(1, 23)) == OrderPrice(OrderPriceType.NET_DEBIT, Amount(1, 23))

        assert OrderPrice(OrderPriceType.NET_EVEN) == OrderPrice(OrderPriceType.NET_DEBIT, ZERO)
        assert OrderPrice(OrderPriceType.NET_EVEN) == OrderPrice(OrderPriceType.NET_CREDIT, ZERO)

    def test_non_equality_diff_order_price_type(self):
            assert OrderPrice(OrderPriceType.NET_CREDIT, Amount(1, 23)) != OrderPrice(OrderPriceType.NET_DEBIT,
                                                                                      Amount(1, 23))

    def test_gt(self):
        assert OrderPrice(OrderPriceType.NET_EVEN) > OrderPrice(OrderPriceType.NET_DEBIT, Amount(0,1))
        assert OrderPrice(OrderPriceType.NET_CREDIT, Amount(0,1)) > OrderPrice(OrderPriceType.NET_DEBIT, Amount(0, 1))
        assert OrderPrice(OrderPriceType.NET_CREDIT, Amount(0,2)) > OrderPrice(OrderPriceType.NET_CREDIT, Amount(0, 1))


    def test_lt(self):
        assert OrderPrice(OrderPriceType.NET_EVEN) < OrderPrice(OrderPriceType.NET_CREDIT, Amount(0,1))

    def test_lt_two_debits(self):
        assert OrderPrice(OrderPriceType.NET_DEBIT, Amount(0,2)) < OrderPrice(OrderPriceType.NET_DEBIT, Amount(0, 1))
