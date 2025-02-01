from datetime import datetime

from common.exchange.market_session import MarketSession
from common.finance.amount import Amount
from common.finance.equity import Equity
from common.finance.exercise_style import ExerciseStyle
from common.finance.option import Option
from common.finance.option_type import OptionType
from common.finance.price import Price
from common.finance.tradable import Tradable
from common.order.action import Action
from common.order.executed_order import ExecutedOrder
from common.order.executed_order_details import ExecutionOrderDetails
from common.order.expiry.fill_or_kill import FillOrKill
from common.order.expiry.good_for_day import GoodForDay
from common.order.expiry.good_for_sixty_days import GoodForSixtyDays
from common.order.expiry.good_until_cancelled import GoodUntilCancelled
from common.order.expiry.good_until_date import GoodUntilDate
from common.order.expiry.order_expiry import OrderExpiry
from common.order.order import Order
from common.order.order_line import OrderLine
from common.order.order_price import OrderPrice
from common.order.order_price_type import OrderPriceType
from common.order.order_status import OrderStatus
from common.order.placed_order import PlacedOrder
from common.order.placed_order_details import PlacedOrderDetails
from common.order.tradable_type import TradableType


class OrderConversionUtil:

    @staticmethod
    def to_executed_order_from_json(input_order: dict):
        placed_order: PlacedOrder = OrderConversionUtil.to_placed_order_from_json(input_order)

        order_detail = input_order["OrderDetail"][0]
        execution_order_details: ExecutionOrderDetails = ExecutionOrderDetails(
        Amount.from_float(order_detail["orderValue"]), datetime.fromtimestamp(order_detail["executedTime"] / 1000))

        return ExecutedOrder(placed_order, execution_order_details)

    @staticmethod
    def to_placed_order_from_json(input_order: dict, query_account_id = None, query_order_id: str = None)->PlacedOrder:
        order_id = input_order["orderId"] if "orderId" in input_order else query_order_id
        order_detail = input_order["OrderDetail"][0]
        account_id = order_detail["accountId"] if "accountId" in order_detail else query_account_id
        order: Order = OrderConversionUtil.to_order_from_json(order_detail)

        status: OrderStatus = OrderStatus[str(order_detail['status']).upper()]
        order_placed_time: datetime = datetime.fromtimestamp(order_detail["placedTime"] / 1000)
        replaces_order_id = order_detail['replacesOrderId'] if 'replacesOrderId' in order_detail else None
        market_session = MarketSession[order_detail["marketSession"]]
        ratio = order_detail['ratio'] if 'ratio' in order_detail else None

        # TODO: These seem to be zero .. not sure if that's an after-hours issue, or something more fundamental
        mark_price = order_detail['netPrice']
        bid_price = order_detail['netBid']
        ask_price = order_detail['netAsk']

        order_market_price = Price(bid_price, ask_price, mark_price)

        placed_order_details = PlacedOrderDetails(account_id, order_id, status, order_placed_time, order_market_price, market_session, replaces_order_id)

        return PlacedOrder(order, placed_order_details)

    @staticmethod
    def to_order_from_json(input_order: dict)->Order:
        expiry: OrderExpiry = OrderConversionUtil.get_expiry_from_order(input_order)

        order_price_type = OrderPriceType[input_order["priceType"]]
        limit_price: OrderPrice = OrderPrice(order_price_type, Amount.from_float(input_order["limitPrice"]))

        order_lines: list[OrderLine] = OrderConversionUtil.process_instrument_to_orderlines(input_order)

        input_order: Order = Order(None, expiry, order_lines, limit_price)
        return input_order

    @staticmethod
    def process_instrument_to_orderlines(order: dict)->list[OrderLine]:
        order_lines: list[OrderLine] = list[OrderLine]()
        for instrument in order["Instrument"]:
            quantity = instrument['orderedQuantity'] if 'orderedQuantity' in instrument else instrument['quantity']
            filled_quantity: int = instrument["filledQuantity"] if "filledQuantity" in instrument else 0
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

                option_expiry = datetime(expiry_year, expiry_month, expiry_day).date()

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
        if order_term == "GOOD_TILL_CANCELLED" or order_term == "GOOD_UNTIL_CANCEL":
            return GoodUntilCancelled(all_or_none)
        if order_term == "GOOD_TILL_DATE":
            # TODO: It's not clear where we get the value for GoodUntilDate
            return GoodUntilDate(datetime.date.today(), all_or_none)

    @staticmethod
    def build_order(order: Order) -> str:

        order_term = "GOOD_FOR_DAY"
        if type(order.expiry) == GoodForDay:
            order_term = "GOOD_FOR_DAY"
        elif type(order.expiry) == GoodForSixtyDays:
            order_term = "GOOD_TILL_DATE"
        elif type(order.expiry) == GoodUntilCancelled:
            order_term = "GOOD_UNTIL_CANCELLED"
        elif type(order.expiry) == FillOrKill:
            order_term = "FILL_OR_KILL"

        instruments = list[str]()
        for order_line in order.order_lines:
            instruments.append(OrderConversionUtil.build_instrument(order_line))

        instrument_xml = "\n".join(instruments)

        return f"""<Order>
                               <allOrNone>{order.expiry.all_or_none}</allOrNone>
                               <priceType>{order.order_price.order_price_type.name}</priceType>
                               <orderTerm>{order_term}</orderTerm>
                               <marketSession>REGULAR</marketSession>
                               <stopPrice />
                               <limitPrice>{order.order_price.price}</limitPrice>
                               {instrument_xml}
                       </Order>
            """

    @staticmethod
    def build_instrument(order_line: OrderLine) -> str:
        product_xml = OrderConversionUtil.build_product_xml(order_line.tradable)
        quantity = order_line.quantity
        action = order_line.action

        # TODO: See if `orderedQuantity` is necessary
        return f"""
               <Instrument>
                 <orderAction>{action.name}</orderAction>
                 <orderedQuantity>{quantity}</orderedQuantity>
                 <quantity>{quantity}</quantity>
                 {product_xml}
               </Instrument>
            """

    @staticmethod
    def build_product_xml(tradable: Tradable) -> str:
        security_type = TradableType[type(tradable).__name__].value[0]
        if type(tradable) is Equity:
            e: Equity = tradable
            symbol = e.ticker

            return f"""<Product>
                             <securityType>{security_type}</securityType>
                             <symbol>{symbol}</symbol>
                           </Product>
                """

        elif type(tradable) is Option:
            o: Option = tradable

            symbol = o.equity.ticker
            strike_price: Amount = o.strike
            call_put = str(o.type.name).upper()

            expiry: datetime = o.expiry
            expiry_day: int = expiry.day
            expiry_month: int = expiry.month
            expiry_year: int = expiry.year

            return f"""<Product>
                             <securityType>{security_type}</securityType>
                             <symbol>{symbol}</symbol>
                             <strikePrice>{strike_price.to_float()}</strikePrice>
                             <expiryDay>{expiry_day}</expiryDay>
                             <expiryMonth>{expiry_month}</expiryMonth>
                             <expiryYear>{expiry_year}</expiryYear>
                             <callPut>{call_put}</callPut>
                           </Product>
                """
        else:
            raise Exception(f"Tradable type not recognized, {type(tradable)}")
