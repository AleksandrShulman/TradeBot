import dataclasses
import decimal

import uuid
from datetime import datetime, date

from flask.json.provider import DefaultJSONProvider
from werkzeug.http import http_date
import typing as t

from common.api.orders.order_list_response import ListOrdersResponse
from common.finance.amount import Amount
from common.finance.equity import Equity
from common.finance.option import Option
from common.finance.price import Price
from common.order.executed_order import ExecutedOrder
from common.order.executed_order_details import ExecutionOrderDetails
from common.order.expiry.order_expiry import OrderExpiry
from common.order.order import Order
from common.order.order_line import OrderLine
from common.order.order_price import OrderPrice
from common.order.placed_order import PlacedOrder
from common.order.placed_order_details import PlacedOrderDetails


class CustomJSONProvider(DefaultJSONProvider):
    def default(self, o: t.Any) -> t.Any:
        if isinstance(o, date):
            return http_date(o)

        if isinstance(o, (decimal.Decimal, uuid.UUID)):
            return str(o)

        if isinstance(o, (ListOrdersResponse)):
            return {
                "order_list": o.order_list
            }

        if isinstance(o, (ExecutedOrder)):
            return {
                "order" : o.order,
                "execution_details": o.execution_details
            }

        if isinstance(o, (ExecutionOrderDetails)):
            return {
                "order_value": o.order_value,
                "executed_time" : o.executed_time
            }

        if isinstance(o, (Amount)):
            return {
                "amount": str(o)
            }

        if isinstance(o, (PlacedOrder)):
            return {
                "order": o.order,
                "placed_order_details": o.placed_order_details
            }

        if isinstance(o, (Order)):
            return {
                "order_id": o.order_id,
                "expiry": o.expiry,
                "order_lines": o.order_lines,
                "order_price": o.order_price
            }

        if isinstance(o, (OrderExpiry)):
            return {
                "expiry_date": o.expiry_date,
                "all_or_none": o.all_or_none
            }

        if isinstance(o, (OrderLine)):
            return {
                "action": str(o.action),
                "tradable": o.tradable,
                "quantity": o.quantity,
                "quantity_filled": o.quantity_filled
            }

        if isinstance(o, (Option)):
            return {
                "expiry": o.expiry,
                "equity": o.equity,
                "type": str(o.type),
                "style": str(o.style),
                "strike": o.strike
            }

        if isinstance(o, (Equity)):
            return {
                "ticker" : o.ticker,
                "company_name": o.company_name
            }

        if isinstance(o, (OrderPrice)):
            return {
                "price": str(o.price),
                "order_price_type": str(o.order_price_type)
            }

        if isinstance(o, (PlacedOrderDetails)):
            return {
                "exchange_order_id": o.exchange_order_id,
                "status": str(o.status),
                "account_id": o.account_id,
                "current_market_price": o.current_market_price,
                "order_placed_time": o.order_placed_time,
                "market_session": str(o.market_session),
                "replaces_order_id": o.replaces_order_id
            }

        if isinstance(o, (Price)):
            return {
                "bid": o.bid,
                "ask": o.ask,
                "market": o.mark,
                "last": o.last if hasattr(o, 'last') else None
            }

        if dataclasses and dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)  # type: ignore[arg-type]

        if hasattr(o, "__html__"):
            return str(o.__html__())

        raise TypeError(f"Object of type {type(o).__name__} is not JSON serializable")
