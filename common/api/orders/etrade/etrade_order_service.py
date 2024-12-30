import json
from datetime import datetime
from statistics import quantiles

from common.api.orders.etrade.converters.order_conversion_util import OrderConversionUtil
from common.api.orders.etrade.etrade_order_response_message import ETradeOrderResponseMessage
from common.api.orders.get_order_request import GetOrderRequest
from common.api.orders.get_order_response import GetOrderResponse
from common.api.orders.order_list_request import OrderListRequest
from common.api.orders.order_list_response import OrderListResponse
from common.api.orders.order_service import OrderService
from common.api.orders.place_orders_request import PlaceOrdersRequest
from common.api.orders.place_orders_response import PlaceOrdersResponse
from common.api.orders.preview_orders_request import PreviewOrdersRequest
from common.api.orders.preview_orders_response import PreviewOrdersResponse, OrderPreview
from common.exchange.etrade.etrade_connector import ETradeConnector
from common.exchange.market_session import MarketSession
from common.finance.amount import Amount
from common.finance.equity import Equity
from common.finance.exercise_style import ExerciseStyle
from common.finance.option import Option
from common.finance.option_type import OptionType
from common.finance.tradable import Tradable
from common.order.action import Action
from common.order.executed_order import ExecutedOrder
from common.order.executed_order_details import ExecutionOrderDetails
from common.order.expiry.fill_or_kill import FillOrKill
from common.order.expiry.good_for_day import GoodForDay
from common.order.expiry.good_for_sixty_days import GoodForSixtyDays
from common.order.expiry.good_until_cancelled import GoodUntilCancelled
from common.order.expiry.order_expiry import OrderExpiry
from common.order.order import Order
from common.order.order_line import OrderLine
from common.order.order_price import OrderPrice
from common.order.order_price_type import OrderPriceType
from common.order.order_status import OrderStatus
from common.order.placed_order import PlacedOrder
from common.order.placed_order_details import PlacedOrderDetails
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

        if list_orders_request.status is not OrderStatus.ANY:
            params["status"] = list_orders_request.status.name

        if exchange_specific_opts:
            for k, v in exchange_specific_opts.items():
                params[k] = v

        url = self.base_url + path
        response = self.session.get(url, params=params)

        parsed_order_list: list[Order] = ETradeOrderService._parse_order_list_response(response, account_id)
        return OrderListResponse(parsed_order_list)

    def get_order(self, get_order_request: GetOrderRequest) -> GetOrderResponse:
        pass

    @staticmethod
    def _build_order(order: Order)->str:

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
            instruments.append(ETradeOrderService._build_instrument(order_line))

        instrument_xml = "\n".join(instruments)

        return f"""<Order>
                           <allOrNone>{order.expiry.all_or_none}</allOrNone>
                           <priceType>{order.order_price.order_price_type.name}</priceType>
                           <orderTerm>{order_term}</orderTerm>
                           <marketSession>{order.market_session.name}</marketSession>
                           <stopPrice />
                           <limitPrice>{order.order_price.price}</limitPrice>
                           {instrument_xml}
                   </Order>
        """

    @staticmethod
    def _build_instrument(order_line: OrderLine) -> str:
        product_xml = ETradeOrderService._build_product_xml(order_line.tradable)
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
    def _build_product_xml(tradable: Tradable)->str:
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

    def preview_orders(self, preview_order_request: PreviewOrdersRequest) -> PreviewOrdersResponse:
        order_type = preview_order_request.order_type
        account_id = preview_order_request.account_id

        client_order_id = preview_order_request.orders[0].client_order_id

        headers = {"Content-Type": "application/xml", "consumerKey": account_id}

        orders_xml: list[str] = []
        for order in preview_order_request.orders:
            orders_xml.append(ETradeOrderService._build_order(order))

        orders_str = "\n".join(orders_xml)

        # TODO: Weave through settings for priceType and possibly others.
        path = f"/v1/accounts/{account_id}/orders/preview.json"
        payload = f"""<PreviewOrderRequest>
                       <orderType>{order_type.name}</orderType>
                         <clientOrderId>{client_order_id}</clientOrderId>
                         {orders_str}
                       </PreviewOrderRequest>"""

        url = self.base_url + path
        response = self.session.post(url, header_auth=True, headers=headers, data=payload)
        print(response)
        return ETradeOrderService._parse_preview_orders_response(response)


    def place_order(self, place_order_request: PlaceOrdersRequest) -> PlaceOrdersResponse:
        order_type = place_order_request.order_type
        account_id = place_order_request.account_id

        client_order_id = place_order_request.orders[0].client_order_id

        headers = {"Content-Type": "application/xml", "consumerKey": account_id}


        preview_ids_xml: list[str] = []
        for preview_id in place_order_request.preview_ids:
            preview_ids_xml.append(f"<previewId>{preview_id}</previewId>")

        orders_xml: list[str] = []
        for order in place_order_request.orders:
            orders_xml.append(ETradeOrderService._build_order(order))

        orders_str = "\n".join(orders_xml)

        preview_ids_str = "\n".join(preview_ids_xml)

        # TODO: Weave through settings for priceType and possibly others.
        path = f"/v1/accounts/{account_id}/orders/place.json"
        payload = f"""<PlaceOrderRequest>
                        <PreviewIds>
                        {preview_ids_str}
                        </PreviewIds>
                        <orderType>{order_type.name}</orderType>
                        <clientOrderId>{client_order_id}</clientOrderId>
                        {orders_str}
                      </PlaceOrderRequest>"""

        url = self.base_url + path
        response = self.session.post(url, header_auth=True, headers=headers, data=payload)
        print(response)
        return ETradeOrderService._parse_place_orders_response(response)

    @staticmethod
    def _parse_place_orders_response(input)-> PlaceOrdersResponse:
        data = json.loads(input.text)
        place_order_response = data["PlaceOrderResponse"]
        order_ids = place_order_response['OrderIds']
        order_dicts = place_order_response["Order"]

        order_ids_to_orders = zip(order_dicts, order_ids)

        messages = []
        for order_dict in order_dicts:
            for message in order_dict['messages']['Message']:
                description = message['description']
                code = message['code']
                message_type = message['type']
                messages.append(ETradeOrderResponseMessage(code, description, message_type))

        orders = [OrderConversionUtil.to_order_from_json(order_dict, order_id["orderId"]) for (order_dict, order_id) in order_ids_to_orders]

        return PlaceOrdersResponse(order_ids, orders, messages)


    @staticmethod
    def _parse_preview_orders_response(input)-> PreviewOrdersResponse:
        data = json.loads(input.text)
        preview_order_response = data["PreviewOrderResponse"]
        order_previews = list()
        preview_ids: list[dict[str:str]] = preview_order_response["PreviewIds"]
        orders: list[dict] = preview_order_response["Order"]
        for index, preview_id in enumerate(preview_ids):
            order_preview = OrderPreview(preview_id, orders[index]["estimatedTotalAmount"], orders[index]["estimatedCommission"])
            order_previews.append(order_preview.preview_id["previewId"])

        return PreviewOrdersResponse(order_previews)

    @staticmethod
    def _parse_order_list_response(response, account_id) -> list[Order]:
        if response.status_code == '204':
            return list[Order]()

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

            order_lines: list[OrderLine] = OrderConversionUtil.process_instrument_to_orderlines(order)
            order_price: OrderPrice = OrderPrice(price_type, limit_price)
            order_placed_time: datetime = datetime.fromtimestamp(order_detail["placedTime"]/1000)

            placed_order_details = PlacedOrderDetails(account_id, status, order_placed_time, replaces_order_id)

            o: Order = Order(order_id, expiry, order_lines, order_price, market_session)

            placed_order: PlacedOrder = PlacedOrder(o, placed_order_details)
            if status == OrderStatus.EXECUTED:
                execution_order_details: ExecutionOrderDetails = ExecutionOrderDetails(Amount.from_float(order_detail["orderValue"]), datetime.fromtimestamp(order_detail["executedTime"]/1000))
                o: ExecutedOrder = ExecutedOrder(placed_order, execution_order_details)
            return_order_list.append(o)

        return return_order_list