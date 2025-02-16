from common.api.test.orders.order_test_util import OrderTestUtil
from common.finance.amount import Amount
from common.finance.equity import Equity
from common.order.order import Order
from common.order.order_price import OrderPrice
from common.order.order_price_type import OrderPriceType
from tex.test.test_get_market_price import equity
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
