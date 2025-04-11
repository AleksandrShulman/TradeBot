import dataclasses
import decimal

import uuid
from datetime import datetime, date

from flask.json.provider import DefaultJSONProvider
from werkzeug.http import http_date
import typing as t

from common.api.orders.get_order_response import GetOrderResponse
from common.api.orders.order_list_response import ListOrdersResponse
from common.api.orders.place_order_response import PlaceOrderResponse
from common.api.orders.preview_order_response import PreviewOrderResponse
from common.api.request_status import RequestStatus
from common.finance.amount import Amount
from common.finance.currency import Currency
from common.finance.equity import Equity
from common.finance.exercise_style import ExerciseStyle
from common.finance.option import Option
from common.finance.price import Price
from common.order.executed_order import ExecutedOrder
from common.order.executed_order_details import ExecutionOrderDetails
from common.order.expiry.order_expiry import OrderExpiry
from common.order.order import Order
from common.order.order_line import OrderLine
from common.order.order_price import OrderPrice
from common.order.order_type import OrderType
from common.order.placed_order import PlacedOrder
from common.order.placed_order_details import PlacedOrderDetails


class CustomJSONProvider(DefaultJSONProvider):
    # TODO: Refactor so as to reference the method from CustomJsonEncoder instead of
    # re-implementing it.
    def default(self, o: t.Any) -> t.Any:
        if isinstance(o, date):
            return http_date(o)

        if isinstance(o, (decimal.Decimal, uuid.UUID)):
            return str(o)

        if isinstance(o, (ListOrdersResponse)):
            return {
                "order_list": o.order_list
            }

        if isinstance(o, (GetOrderResponse)):
            return {
                "placed_order": o.placed_order
            }

        if isinstance(o, (PlaceOrderResponse)):
            return o.model_dump()

        if isinstance(o, (PreviewOrderResponse)):
            return o.model_dump()

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

        if isinstance(o, (OrderType)):
            return str(o)

        if isinstance(o, ExerciseStyle):
            return str(o)
        if isinstance(o, (Currency)):
            return str(o)

        if isinstance(o, (RequestStatus)):
            return {
                "request_status": str(o)
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

