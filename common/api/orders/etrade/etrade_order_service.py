import json
import pickle
from datetime import datetime

from common.api.orders.cancel_order_request import CancelOrderRequest
from common.api.orders.cancel_order_response import CancelOrderResponse
from common.api.orders.etrade.converters.order_conversion_util import OrderConversionUtil
from common.api.orders.etrade.etrade_order_response_message import ETradeOrderResponseMessage
from common.api.orders.get_order_request import GetOrderRequest
from common.api.orders.get_order_response import GetOrderResponse
from common.api.orders.modify_order_request import ModifyOrderRequest
from common.api.orders.modify_order_response import ModifyOrderResponse, OrderModification
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
from common.finance.option import Option
from common.finance.tradable import Tradable
from common.order.executed_order import ExecutedOrder
from common.order.executed_order_details import ExecutionOrderDetails
from common.order.expiry.fill_or_kill import FillOrKill
from common.order.expiry.good_for_day import GoodForDay
from common.order.expiry.good_for_sixty_days import GoodForSixtyDays
from common.order.expiry.good_until_cancelled import GoodUntilCancelled
from common.order.order import Order
from common.order.order_line import OrderLine
from common.order.order_price import OrderPrice
from common.order.order_price_type import OrderPriceType
from common.order.order_status import OrderStatus
from common.order.order_type import OrderType
from common.order.placed_order import PlacedOrder
from common.order.placed_order_details import PlacedOrderDetails
from common.order.tradable_type import TradableType


class ETradeOrderService(OrderService):
    def __init__(self, connector: ETradeConnector):
        super().__init__(connector)
        self.session, self.base_url = self.connector.load_connection()

    def list_orders(self, list_orders_request: OrderListRequest, exchange_specific_opts: dict[str, str]) -> OrderListResponse:
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

    def cancel_order(self, cancel_order_request: CancelOrderRequest) -> CancelOrderResponse:
        account_id = cancel_order_request.account_id
        order_id = cancel_order_request.order_id

        headers = {"Content-Type": "application/xml", "consumerKey": account_id}

        # TODO: Weave through settings for priceType and possibly others.
        path = f"/v1/accounts/{account_id}/orders/cancel.json"
        payload = f"""
            <CancelOrderRequest>
              <orderId>{order_id}</orderId>
            </CancelOrderRequest>"""

        url = self.base_url + path
        response = self.session.put(url, header_auth=True, headers=headers, data=payload)
        print(response)
        return ETradeOrderService._parse_cancel_order_response(response)

    def modify_order(self, modify_order_request: ModifyOrderRequest) -> ModifyOrderResponse:
        preview_order_request = modify_order_request.preview_orders_request
        order_type = preview_order_request.order_type
        account_id = preview_order_request.account_id
        client_order_id = preview_order_request.orders[0].client_order_id
        order_id = modify_order_request.order_id

        headers = {"Content-Type": "application/xml", "consumerKey": account_id}

        # TODO: Weave through settings for priceType and possibly others.
        path = f"/v1/accounts/{account_id}/orders/{order_id}/change/preview.json"

        payload = ETradeOrderService._build_preview_order_xml(preview_order_request.orders, order_type, client_order_id)

        url = self.base_url + path
        response = self.session.put(url, header_auth=True, headers=headers, data=payload)
        print(response)
        return ETradeOrderService._parse_modify_order_response(response)

    def preview_orders(self, preview_order_request: PreviewOrdersRequest) -> PreviewOrdersResponse:
        order_type = preview_order_request.order_type
        account_id = preview_order_request.account_id
        client_order_id = preview_order_request.orders[0].client_order_id

        headers = {"Content-Type": "application/xml", "consumerKey": account_id}
        path = f"/v1/accounts/{account_id}/orders/preview.json"

        payload = ETradeOrderService._build_preview_order_xml(preview_order_request.orders, order_type, client_order_id)

        url = self.base_url + path
        response = self.session.post(url, header_auth=True, headers=headers, data=payload)
        print(response)
        #with open('output_preview_order_spread', 'wb') as handle:
        #    pickle.dump(response, handle, protocol=pickle.HIGHEST_PROTOCOL)

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
            orders_xml.append(OrderConversionUtil.build_order(order))

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
        with open('output_place_order_spread', 'wb') as handle:
            pickle.dump(response, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print(response)
        return ETradeOrderService._parse_place_orders_response(response, client_order_id)

    @staticmethod
    def _parse_place_orders_response(input, client_order_id: str)-> PlaceOrdersResponse:
        data = json.loads(input.text)
        place_order_response = data["PlaceOrderResponse"]
        order_ids: list[str] = [order_id["orderId"] for order_id in place_order_response['OrderIds']]
        order_dicts = place_order_response["Order"]

        order_ids_to_orders = zip(order_dicts, order_ids)

        messages = []
        for order_dict in order_dicts:
            for message in order_dict['messages']['Message']:
                description = message['description']
                code = message['code']
                message_type = message['type']
                messages.append(ETradeOrderResponseMessage(code, description, message_type))

        orders = [OrderConversionUtil.to_order_from_json(order_dict, order_id, client_order_id) for (order_dict, order_id) in order_ids_to_orders]

        return PlaceOrdersResponse(order_ids, orders, messages)

    def _parse_cancel_order_response(input)-> CancelOrderResponse:
        data = json.loads(input.text)
        cancel_order_response = data["CancelOrderResponse"]

        order_id = cancel_order_response["orderId"]
        cancel_time = cancel_order_response["cancelTime"]

        messages = []
        for message in cancel_order_response['Messages']['Message']:
            description = message['description']
            code = message['code']
            message_type = message['type']
            messages.append(ETradeOrderResponseMessage(code, description, message_type))

        return CancelOrderResponse(order_id, cancel_time, messages)

    @staticmethod
    def _parse_preview_orders_response(input)-> PreviewOrdersResponse:
        data = json.loads(input.text)
        preview_order_response = data["PreviewOrderResponse"]
        order_previews: list[OrderPreview] = list()
        preview_ids: list[dict[str:str]] = preview_order_response["PreviewIds"]
        orders: list[dict] = preview_order_response["Order"]
        for index, preview_id in enumerate(preview_ids):
            order_preview: OrderPreview = OrderPreview(preview_id["previewId"],
                                                       Amount.from_float(orders[index]["estimatedTotalAmount"]),
                                                       Amount.from_float(orders[index]["estimatedCommission"]))
            order_previews.append(order_preview)

        return PreviewOrdersResponse(order_previews)

    @staticmethod
    def _parse_order_list_response(response, account_id) -> list[PlacedOrder]:
        if response.status_code == '204':
            return list[PlacedOrder]()

        data = response.json()
        print(data)

        return_order_list: list[PlacedOrder] = []

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
                executed_order: ExecutedOrder = ExecutedOrder(placed_order, execution_order_details)

                # TODO: Build an interface that all orders (executed, placed, or just plain) can use so that I categorize them as such
                return_order_list.append(executed_order)
            else:
                return_order_list.append(placed_order)

        return return_order_list

    @staticmethod
    def _parse_modify_order_response(input):
        data = json.loads(input.text)
        modify_order_response = data["PreviewOrderResponse"]
        order_modifications = list()
        preview_ids: list[dict[str:str]] = modify_order_response["PreviewIds"]
        orders: list[dict] = modify_order_response["Order"]
        for index, preview_id in enumerate(preview_ids):
            order_modification = OrderModification(orders[index], preview_id)
            order_modifications.append(order_modification.preview_id["previewId"])

        return ModifyOrderResponse(order_modifications)


    @staticmethod
    def _build_preview_order_xml(orders, order_type: OrderType, client_order_id: str)->str:
        orders_xml: list[str] = []
        for order in orders:
            orders_xml.append(OrderConversionUtil.build_order(order))

        orders_str = "\n".join(orders_xml)
        return f"""<PreviewOrderRequest>
                               <orderType>{order_type.name}</orderType>
                                 <clientOrderId>{client_order_id}</clientOrderId>
                                 {orders_str}
                               </PreviewOrderRequest>"""

