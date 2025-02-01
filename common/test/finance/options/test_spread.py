from datetime import datetime

import pytest

from common.finance.amount import Amount
from common.finance.currency import Currency
from common.finance.equity import Equity
from common.finance.option import Option
from common.finance.option_type import OptionType
from common.finance.options.equity_order_line import EquityOrderLine
from common.finance.options.mixed.buy_write import BuyWrite
from common.finance.options.option_order_line import OptionOrderLine
from common.finance.options.spread import Spread, DE_NORMALIZATION_CONSTANT
from common.order.action import Action
from common.order.order_line import OrderLine
from common.order.order_price import OrderPrice
from common.order.order_price_type import OrderPriceType


class TestSpread:

    @pytest.fixture
    def sfix_covered_call(self):
        equity = Equity("SFIX", "STITCH FIX INC COM CL A")
        option_expiry: datetime.date = datetime(2025, 1, 31).date()
        tradable1: Option = Option(equity, OptionType.CALL, Amount(4, 0, Currency.US_DOLLARS), option_expiry)

        ol_1 = EquityOrderLine(equity, Action.BUY, 100)
        ol_2 = OptionOrderLine(tradable1, Action.SELL_OPEN, 1)

        order_price: OrderPrice = OrderPrice(OrderPriceType.NET_CREDIT, Amount(0, 44))

        option_order_lines: list[OrderLine] = list[OrderLine]()

        option_order_lines.append(ol_2)

        return BuyWrite(order_price, ol_1, option_order_lines)

    @pytest.fixture
    def sfix_call_credit_spread(self) -> Spread:
        equity = Equity("SFIX", "STITCH FIX INC COM CL A")
        option_expiry: datetime.date = datetime(2025, 1, 31).date()
        tradable1: Option = Option(equity, OptionType.CALL, Amount(4, 0, Currency.US_DOLLARS), option_expiry)
        tradable2: Option = Option(equity, OptionType.CALL, Amount(5, 0, Currency.US_DOLLARS), option_expiry)

        ol_1 = OrderLine(tradable1, Action.SELL_OPEN, 1)
        ol_2 = OrderLine(tradable2, Action.BUY_OPEN, 1)

        order_price: OrderPrice = OrderPrice(OrderPriceType.NET_CREDIT, Amount(0, 44))

        order_lines: list[OrderLine] = list[OrderLine]()
        order_lines.append(ol_1)
        order_lines.append(ol_2)

        return Spread(order_price, order_lines)

    @pytest.fixture
    def sfix_call_debit_diagonal_spread(self) -> Spread:
        equity = Equity("SFIX", "STITCH FIX INC COM CL A")
        option_expiry_1: datetime.date = datetime(2025, 1, 31).date()
        option_expiry_2: datetime.date = datetime(2025, 2, 6).date()
        tradable1: Option = Option(equity, OptionType.CALL, Amount(4, 0, Currency.US_DOLLARS), option_expiry_1)
        tradable2: Option = Option(equity, OptionType.CALL, Amount(5, 0, Currency.US_DOLLARS), option_expiry_2)

        ol_1 = OrderLine(tradable1, Action.SELL_OPEN, 1)
        ol_2 = OrderLine(tradable2, Action.BUY_OPEN, 1)

        order_price: OrderPrice = OrderPrice(OrderPriceType.NET_DEBIT, Amount(0, 5))

        order_lines: list[OrderLine] = list[OrderLine]()
        order_lines.append(ol_1)
        order_lines.append(ol_2)

        return Spread(order_price, order_lines)

    @pytest.fixture
    def sfix_put_credit_calendar_spread(self) -> Spread:
        equity = Equity("SFIX", "STITCH FIX INC COM CL A")
        option_expiry_1: datetime.date = datetime(2025, 1, 31).date()
        option_expiry_2: datetime.date = datetime(2025, 2, 6).date()
        tradable1: Option = Option(equity, OptionType.PUT, Amount(5, 0, Currency.US_DOLLARS), option_expiry_1)
        tradable2: Option = Option(equity, OptionType.PUT, Amount(5, 0, Currency.US_DOLLARS), option_expiry_2)

        ol_1 = OrderLine(tradable1, Action.BUY_OPEN, 1)
        ol_2 = OrderLine(tradable2, Action.SELL_OPEN, 1)

        order_price: OrderPrice = OrderPrice(OrderPriceType.NET_CREDIT, Amount(0, 5))

        order_lines: list[OrderLine] = list[OrderLine]()
        order_lines.append(ol_1)
        order_lines.append(ol_2)

        return Spread(order_price, order_lines)

    @pytest.fixture
    def sfix_call_debit_spread(self) -> Spread:
        equity = Equity("SFIX", "STITCH FIX INC COM CL A")
        option_expiry: datetime.date = datetime(2025, 1, 31).date()
        tradable1: Option = Option(equity, OptionType.CALL, Amount(4, 0, Currency.US_DOLLARS), option_expiry)
        tradable2: Option = Option(equity, OptionType.CALL, Amount(5, 0, Currency.US_DOLLARS), option_expiry)

        ol_1 = OrderLine(tradable1, Action.BUY_OPEN, 1)
        ol_2 = OrderLine(tradable2, Action.SELL_OPEN, 1)

        order_price: OrderPrice = OrderPrice(OrderPriceType.NET_DEBIT, Amount(0, 44))

        order_lines: list[OrderLine] = list[OrderLine]()
        order_lines.append(ol_1)
        order_lines.append(ol_2)

        return Spread(order_price, order_lines)

    def test_vertical_call_credit_spread_collateral_requirement(self, sfix_call_credit_spread: Spread):
        expected_collateral_required = Amount(100, 0) - Amount(0, 44) * DE_NORMALIZATION_CONSTANT
        collateral_required: Amount = sfix_call_credit_spread.get_collateral_required()

        assert collateral_required == expected_collateral_required

    def test_diagonal_call_debit_spread_collateral_requirement(self, sfix_call_debit_diagonal_spread: Spread):
        expected_collateral_required = Amount(100, 0) + Amount(0, 5) * DE_NORMALIZATION_CONSTANT
        collateral_required: Amount = sfix_call_debit_diagonal_spread.get_collateral_required()

        assert collateral_required == expected_collateral_required

    def test_put_calendar_credit_spread_collateral_requirement(self, sfix_put_credit_calendar_spread: Spread):
        expected_collateral_required = Amount(500, 0) - Amount(0, 5) * DE_NORMALIZATION_CONSTANT
        collateral_required: Amount = sfix_put_credit_calendar_spread.get_collateral_required()

        assert collateral_required == expected_collateral_required


    def test_vertical_call_debit_spread_collateral_requirement(self, sfix_call_debit_spread: Spread):
        expected_collateral_required = Amount(0, 44) * DE_NORMALIZATION_CONSTANT
        collateral_required: Amount = sfix_call_debit_spread.get_collateral_required()

        assert collateral_required == expected_collateral_required


    def test_diagonal_put_spread_collateral_requirement(self):
        pass

    def test_call_spread_vertical_spread_collateral_requirement(self):
        pass

    def test_spread_to_order(self):
        pass

    def test_order_to_spread(self):
        pass