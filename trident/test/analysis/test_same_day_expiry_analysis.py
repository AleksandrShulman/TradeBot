import pytest

from common.api.test.orders.order_test_util import OrderTestUtil
from common.finance.amount import Amount
from common.finance.equity import Equity
from common.order.order import Order
from common.order.order_price import OrderPrice
from common.order.order_price_type import OrderPriceType
from common.order.tradable_type import TradableType
from trident.analysis.same_expiry_combined_order_analyser import SameDayExpiryCombinedOrderAnalyser


class TestSameDayExpiryAnalysis:
    def test_option_spread(self):
        spread_order: Order = OrderTestUtil.build_spread_order(order_price = OrderPrice(OrderPriceType.NET_CREDIT, Amount(1, 50)))
        tradable = spread_order.order_lines[0].tradable
        equity: Equity = tradable if isinstance(tradable, Equity) else tradable.equity

        at_price: float = Amount(157, 50).to_float()

        analyser = SameDayExpiryCombinedOrderAnalyser(equity, [spread_order])

        assert analyser.get_value_for_given_price_at_expiry(at_price) == Amount(250, 0, negative=True)
        assert analyser.get_pl_for_given_price_at_expiry(at_price) == Amount(100, 0, negative=True)

    @pytest.mark.parametrize("closing_option_desc,equity_price,expected_order_value,expected_pl", [(("otm"), Amount(3, 95), Amount(395,0), Amount(11,0)),
                                                                                     (("atm"), Amount(4, 0), Amount(400,0), Amount(16,0)),
                                                                                     (("atm"), Amount(4, 5), Amount(400,0), Amount(16, 0))])
    def test_covered_call(self, closing_option_desc: str, equity_price: Amount, expected_order_value: Amount, expected_pl: Amount):
        covered_call_order: Order = OrderTestUtil.build_covered_call()
        equity: Equity = list(filter(lambda ol: ol.tradable.get_type() == TradableType.Equity, covered_call_order.order_lines))[0].tradable

        analyser = SameDayExpiryCombinedOrderAnalyser(equity, [covered_call_order])

        analysed_order_value = analyser.get_value_for_given_price_at_expiry(equity_price.to_float())
        assert analysed_order_value == expected_order_value
        assert analyser.get_pl_for_given_price_at_expiry(equity_price.to_float()) == expected_pl

    @pytest.mark.parametrize("closing_option_desc,equity_price,expected_order_value,expected_pl", [(("a"), Amount(5, 15), Amount(100,0, negative=True), Amount(41,0, negative=True)),
                                                                                     ("b", Amount(4, 75), Amount(75,0, negative=True), Amount(16,0, negative=True)),
                                                                                     ("c", Amount(4, 0), Amount(0,0), Amount(59, 0)),
                                                                                     ("d", Amount(3, 15), Amount(85, 0, negative=True), Amount(26, 0, negative=True)),
                                                                                     ("e", Amount(2, 95), Amount(100, 0, negative=True), Amount(41, 0, negative=True))])
    def test_iron_butterfly(self, closing_option_desc: str, equity_price: Amount, expected_order_value: Amount, expected_pl: Amount):
        covered_call_order: Order = OrderTestUtil.build_iron_butterfly()
        equity = Equity("SFIX", "STITCH FIX INC COM CL A")

        analyser = SameDayExpiryCombinedOrderAnalyser(equity, [covered_call_order])

        analysed_order_value = analyser.get_value_for_given_price_at_expiry(equity_price.to_float())
        assert analysed_order_value == expected_order_value
        assert analyser.get_pl_for_given_price_at_expiry(equity_price.to_float()) == expected_pl