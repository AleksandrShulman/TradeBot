import datetime

from common.exchange.market_session import MarketSession
from common.finance.amount import Amount
from common.finance.equity import Equity
from common.finance.exercise_style import ExerciseStyle
from common.finance.option import Option
from common.finance.option_type import OptionType
from common.order.action import Action
from common.order.expiry.good_for_day import GoodForDay
from common.order.expiry.good_until_cancelled import GoodUntilCancelled
from common.order.expiry.good_until_date import GoodUntilDate
from common.order.expiry.order_expiry import OrderExpiry
from common.order.order import Order
from common.order.order_line import OrderLine
from common.order.order_price import OrderPrice
from common.order.order_price_type import OrderPriceType
from common.order.tradable_type import TradableType


class OrderConversionUtil:

    @staticmethod
    def to_order_from_json(order: dict, order_id: str)->Order:

        expiry: OrderExpiry = OrderConversionUtil.get_expiry_from_order(order)

        order_price_type = OrderPriceType[order["priceType"]].name
        limit_price: OrderPrice = OrderPrice(order_price_type, Amount.from_float(order["limitPrice"]))
        market_session = MarketSession[order["marketSession"]].name

        order_lines: list[OrderLine] = OrderConversionUtil.process_instrument_to_orderlines(order)

        order: Order = Order(order_id, expiry, order_lines, limit_price, market_session)
        return order

    @staticmethod
    def process_instrument_to_orderlines(order: dict)->list[OrderLine]:
        order_lines: list[OrderLine] = list[OrderLine]()
        for instrument in order["Instrument"]:
            quantity = instrument['quantity']
            filled_quantity = instrument["filledQuantity"] if "filledQuantity" in instrument else None
            order_action = Action[instrument['orderAction']]
            product = instrument["Product"]
            symbol = product['symbol']
            equity = Equity(symbol, None)
            security_type = product["securityType"]

            if security_type == TradableType.Equity.value[0]:
                order_lines.append(OrderLine(equity, order_action, quantity, filled_quantity))
            elif security_type == TradableType.Option.value[0]:
                call_put: OptionType = OptionType.from_str(product['callPut'])
                expiry_year = product['expiryYear']
                expiry_month = product['expiryMonth']
                expiry_day = product['expiryDay']
                strike_price = Amount.from_float(product['strikePrice'])

                option_expiry = datetime.datetime(expiry_year, expiry_month, expiry_day).date()

                o: Option = Option(equity, call_put, strike_price, option_expiry, ExerciseStyle.from_ticker(symbol))
                order_lines.append(OrderLine(o, order_action, quantity, filled_quantity))
            else:
                raise Exception(f"Could not parse info for security type {security_type}")

        return order_lines

    @staticmethod
    def to_xml_from_order(order: Order)->str:
        pass

    @staticmethod
    def get_expiry_from_order(json: dict) -> OrderExpiry:
        all_or_none: bool = json["allOrNone"]
        order_term = json["orderTerm"]
        if order_term == "GOOD_FOR_DAY":
            return GoodForDay()
        if order_term == "GOOD_TILL_CANCELLED":
            return GoodUntilCancelled(all_or_none)
        if order_term == "GOOD_TILL_DATE":
            # TODO: It's not clear where we get the value for GoodUntilDate
            return GoodUntilDate(datetime.date.today(), all_or_none)

"""

"Order": [
            {
                "orderTerm": "GOOD_FOR_DAY",
                "priceType": "LIMIT",
                "limitPrice": 100,
                "stopPrice": 0,
                "marketSession": "REGULAR",
                "allOrNone": false,
                "messages": {
                    "Message": [
                        {
                            "description": "200|The market was closed when we received your order. It has been entered into our system and will be reviewed prior to market open on the next regular trading day. After market open, please check to make sure your order was accepted.",
                            "code": 1027,
                            "type": "WARNING"
                        }
                    ]
                },
                "egQual": "EG_QUAL_UNSPECIFIED",
                "estimatedCommission": 0,
                "estimatedTotalAmount": 500,
                "netPrice": 0,
                "netBid": 0,
                "netAsk": 0,
                "gcd": 0,
                "ratio": "",
                "Instrument": [
                    {
                        "symbolDescription": "GE AEROSPACE COM NEW",
                        "orderAction": "BUY",
                        "quantityType": "QUANTITY",
                        "quantity": 5,
                        "cancelQuantity": 0,
                        "reserveOrder": true,
                        "reserveQuantity": 0,
                        "Product": {
                            "symbol": "GE",
                            "securityType": "EQ"
                        }
                    }
                ]
            }
        ]
"""