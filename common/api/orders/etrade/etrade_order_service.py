from datetime import datetime
from statistics import quantiles

from common.api.orders.get_order_request import GetOrderRequest
from common.api.orders.get_order_response import GetOrderResponse
from common.api.orders.order_list_request import OrderListRequest
from common.api.orders.order_list_response import OrderListResponse
from common.api.orders.order_service import OrderService
from common.api.orders.place_order_request import PlaceOrderRequest
from common.api.orders.place_order_response import PlaceOrderResponse
from common.exchange.etrade.etrade_connector import ETradeConnector
from common.exchange.market_session import MarketSession
from common.finance.amount import Amount
from common.finance.equity import Equity
from common.finance.exercise_style import ExerciseStyle
from common.finance.option import Option
from common.finance.option_type import OptionType
from common.order.action import Action
from common.order.executed_order import ExecutedOrder
from common.order.executed_order_details import ExecutionOrderDetails
from common.order.expiry.good_until_cancelled import GoodUntilCancelled
from common.order.expiry.order_expiry import OrderExpiry
from common.order.order import Order
from common.order.order_line import OrderLine
from common.order.order_price import OrderPrice
from common.order.order_price_type import OrderPriceType
from common.order.order_status import OrderStatus
from common.order.tradable_type import TradableType


class ETradeOrderService(OrderService):
    def __init__(self, connector: ETradeConnector):
        super().__init__(connector)
        self.session, self.base_url = self.connector.load_connection()

    def list_orders(self, list_orders_request: OrderListRequest, exchange_specific_opts: dict[str, str]) -> OrderListResponse:
        #account_id = list_orders_request.account_id
        account_id = list_orders_request.account_id
        path = f"/v1/accounts/{account_id}/orders.json"
        count = list_orders_request.count

        params = dict()
        params["count"] = count
        params["fromDate"] = list_orders_request.from_date.strftime("%m%d%Y")
        params["toDate"] = list_orders_request.to_date.strftime("%m%d%Y")

        if exchange_specific_opts:
            for k, v in list_orders_request.items():
                params[k] = v

        url = self.base_url + path
        response = self.session.get(url, params=params)

        parsed_order_list: list[Order] = ETradeOrderService._parse_order_list_response(response, account_id)
        return OrderListResponse(parsed_order_list)

    def get_order(self, get_order_request: GetOrderRequest) -> GetOrderResponse:
        pass

    def place_order(self, place_order_request: PlaceOrderRequest) -> PlaceOrderResponse:
        pass

    @staticmethod
    def _parse_order_list_response(response, account_id) -> list[Order]:
        data = response.json()
        print(data)

        return_order_list: list[Order] = []

        orders_response = data["OrdersResponse"]
        orders = orders_response['Order']
        for order in orders:
            order_id = order['orderId']
            order_detail = order['OrderDetail'][0]
            status: OrderStatus = OrderStatus[str(order_detail['status']).upper()]
            price_type: OrderPriceType = OrderPriceType[str(order_detail['priceType'])]
            all_or_none: bool = order_detail['allOrNone']
            market_session: MarketSession = MarketSession[str(order_detail['marketSession'])]
            expiry = None
            order_term = order_detail['orderTerm']
            limit_price: Amount = Amount.from_float(order_detail['limitPrice']) if 'limitPrice' in order_detail else None
            replaces_order_id = order_detail['replacesOrderId'] if 'replacesOrderId' in order_detail else None
            if order_term == "GOOD_UNTIL_CANCEL":
                expiry = GoodUntilCancelled(all_or_none)

            instruments = order_detail['Instrument']
            order_lines: list[OrderLine] = []
            for instrument in instruments:

                product = instrument['Product']
                security_type = product['securityType']
                symbol = product['symbol']
                equity = Equity(symbol, None)

                order_action = Action[instrument['orderAction']]
                quantity = instrument['orderedQuantity']
                quantity_filled = instrument['filledQuantity']

                if security_type == TradableType.Option.value[0]:
                    call_put: OptionType = OptionType.from_str(product['callPut'])
                    expiry_year = product['expiryYear']
                    expiry_month = product['expiryMonth']
                    expiry_day = product['expiryDay']
                    strike_price = Amount.from_float(product['strikePrice'])

                    expiry = OrderExpiry(datetime(expiry_year, expiry_month, expiry_day).date(), all_or_none)

                    o: Option = Option(equity, call_put, strike_price, expiry, ExerciseStyle.from_ticker(symbol))
                    order_lines.append(OrderLine(o, order_action, quantity, quantity_filled))
                elif security_type == TradableType.Equity.name:
                    order_lines.append(OrderLine(equity, order_action, quantity, quantity_filled))


            order_price: OrderPrice = OrderPrice(price_type, limit_price)

            o: Order = Order(order_id, account_id, status, expiry, order_lines, order_price, market_session, replaces_order_id)
            if status == OrderStatus.EXECUTED:
                execution_order_details: ExecutionOrderDetails = ExecutionOrderDetails(Amount.from_float(order_detail["orderValue"]), datetime.fromtimestamp(order_detail["executedTime"]/1000))
                o: ExecutedOrder = ExecutedOrder(o, execution_order_details)
            return_order_list.append(o)

        return return_order_list