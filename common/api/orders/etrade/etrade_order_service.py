import json

from common.api.orders.cancel_order_request import CancelOrderRequest
from common.api.orders.cancel_order_response import CancelOrderResponse
from common.api.orders.etrade.converters.order_conversion_util import OrderConversionUtil
from common.api.orders.etrade.etrade_order_response_message import ETradeOrderResponseMessage
from common.api.orders.get_order_request import GetOrderRequest
from common.api.orders.get_order_response import GetOrderResponse
from common.api.orders.order_list_request import ListOrdersRequest
from common.api.orders.order_list_response import ListOrdersResponse
from common.api.orders.order_metadata import OrderMetadata
from common.api.orders.order_preview import OrderPreview
from common.api.orders.order_service import OrderService
from common.api.orders.place_modify_order_request import PlaceModifyOrderRequest
from common.api.orders.place_modify_order_response import PlaceModifyOrderResponse
from common.api.orders.place_order_request import PlaceOrderRequest
from common.api.orders.place_order_response import PlaceOrderResponse
from common.api.orders.preview_modify_order_request import PreviewModifyOrderRequest
from common.api.orders.preview_modify_order_response import PreviewModifyOrderResponse
from common.api.orders.preview_order_request import PreviewOrderRequest
from common.api.orders.preview_order_response import PreviewOrderResponse
from common.exchange.etrade.etrade_connector import ETradeConnector
from common.finance.amount import Amount
from common.order.order import Order
from common.order.order_status import OrderStatus
from common.order.order_type import OrderType
from common.order.placed_order import PlacedOrder


class ETradeOrderService(OrderService):
    def __init__(self, connector: ETradeConnector):
        super().__init__(connector)
        self.session, self.base_url = self.connector.load_connection()

    def list_orders(self, list_orders_request: ListOrdersRequest, exchange_specific_opts: dict[str, str]) -> ListOrdersResponse:
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
        return ListOrdersResponse(parsed_order_list)

    def get_order(self, get_order_request: GetOrderRequest) -> GetOrderResponse:
        account_id = get_order_request.account_id
        order_id = get_order_request.order_id
        path = f"/v1/accounts/{account_id}/orders/{order_id}.json"

        params = dict()
        params["status"] = "OPEN"

        url = self.base_url + path
        response = self.session.get(url, params=params)

        return ETradeOrderService._parse_get_order_response(response, account_id, order_id)

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

    def preview_modify_order(self, preview_modify_order_request: PreviewModifyOrderRequest) -> PreviewModifyOrderResponse:
        order_metadata: OrderMetadata = preview_modify_order_request.order_metadata
        order_type = order_metadata.order_type
        account_id = order_metadata.account_id
        client_order_id = order_metadata.client_order_id

        order_id_to_modify = preview_modify_order_request.order_id_to_modify
        new_order = preview_modify_order_request.order

        headers = {"Content-Type": "application/xml", "consumerKey": account_id}
        path = f"/v1/accounts/{account_id}/orders/{order_id_to_modify}/change/preview.json"

        payload = ETradeOrderService._build_preview_order_xml(new_order, order_type, client_order_id)

        url = self.base_url + path
        response = self.session.put(url, header_auth=True, headers=headers, data=payload)
        return ETradeOrderService._parse_preview_order_response(response, order_metadata, order_id_to_modify)

    def preview_order(self, preview_order_request: PreviewOrderRequest) -> PreviewOrderResponse:
        order_metadata = preview_order_request.order_metadata
        order_type = order_metadata.order_type
        account_id = order_metadata.account_id
        client_order_id = order_metadata.client_order_id

        headers = {"Content-Type": "application/xml", "consumerKey": account_id}
        path = f"/v1/accounts/{account_id}/orders/preview.json"

        payload = ETradeOrderService._build_preview_order_xml(preview_order_request.order, order_type, client_order_id)

        url = self.base_url + path
        response = self.session.post(url, header_auth=True, headers=headers, data=payload)

        return ETradeOrderService._parse_preview_order_response(response, order_metadata)

    def place_modify_order(self, place_modify_order_request: PlaceModifyOrderRequest) -> PlaceModifyOrderResponse:
        order_metadata = place_modify_order_request.order_metadata
        order_type = order_metadata.order_type
        account_id = order_metadata.account_id
        client_order_id = order_metadata.client_order_id

        previous_order_id = place_modify_order_request.order_id_to_modify

        headers = {"Content-Type": "application/xml", "consumerKey": account_id}

        preview_ids_xml: list[str] = []
        orders_xml: list[str] = []
        preview_id = place_modify_order_request.preview_id
        order = place_modify_order_request.order

        preview_ids_xml.append(f"<previewId>{preview_id}</previewId>")
        orders_xml.append(OrderConversionUtil.build_order(order))

        orders_str = "\n".join(orders_xml)
        preview_ids_str = "\n".join(preview_ids_xml)

        path = f"/v1/accounts/{account_id}/orders/{previous_order_id}/change/place.json"

        # TODO: Factor out this payload order so it can be used for order modification
        payload = f"""<PlaceOrderRequest>
                        <PreviewIds>
                        {preview_ids_str}
                        </PreviewIds>
                        <orderType>{order_type.name}</orderType>
                        <clientOrderId>{client_order_id}</clientOrderId>
                        {orders_str}
                      </PlaceOrderRequest>"""

        url = self.base_url + path
        response = self.session.put(url, header_auth=True, headers=headers, data=payload)
        return ETradeOrderService._parse_place_order_response(response, order_metadata, preview_id)

    def place_order(self, place_order_request: PlaceOrderRequest) -> PlaceOrderResponse:
        order_metadata = place_order_request.order_metadata
        order_type = order_metadata.order_type
        account_id = order_metadata.account_id
        client_order_id = order_metadata.client_order_id

        headers = {"Content-Type": "application/xml", "consumerKey": account_id}

        preview_ids_xml: list[str] = []
        orders_xml: list[str] = []
        preview_id = place_order_request.preview_id
        order = place_order_request.order

        preview_ids_xml.append(f"<previewId>{preview_id}</previewId>")
        orders_xml.append(OrderConversionUtil.build_order(order))

        orders_str = "\n".join(orders_xml)
        preview_ids_str = "\n".join(preview_ids_xml)

        path = f"/v1/accounts/{account_id}/orders/place.json"

        # TODO: Factor out this payload order so it can be used for order modification
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
        return ETradeOrderService._parse_place_order_response(response, order_metadata, preview_id)

    def preview_and_place_order(self, preview_order_request: PreviewOrderRequest) -> PlaceOrderResponse:
        order_metadata = preview_order_request.order_metadata
        preview_order_response: PreviewOrderResponse = self.preview_order(preview_order_request)
        preview_id = preview_order_response.preview_id
        place_order_request: PlaceOrderRequest = PlaceOrderRequest(order_metadata, preview_id, preview_order_request.order)
        place_order_response: PlaceOrderResponse = self.place_order(place_order_request)

        return place_order_response

    @staticmethod
    def _parse_place_order_response(response, order_metadata: OrderMetadata, preview_id: str, previous_order_id=None)-> PlaceOrderResponse:
        data = json.loads(response.text)
        place_order_response = data["PlaceOrderResponse"]
        order_type = place_order_response['orderType'] if 'orderType' in place_order_response else None

        if not order_metadata.order_type:
            order_metadata.order_type = order_type

        order_id = place_order_response['OrderIds'][0]["orderId"]
        order_dict = place_order_response["Order"][0]

        messages = []
        for message in order_dict['messages']['Message']:
            description = message['description']
            code = message['code']
            message_type = message['type']
            messages.append(ETradeOrderResponseMessage(code, description, message_type))

        # TODO: Why isn't this a PlacedOrder? b/c 'OrderDetail' isn't available from order_dict here.
        order: Order = OrderConversionUtil.to_order_from_json(order_dict)

        if previous_order_id:
            return PlaceModifyOrderResponse(order_metadata, preview_id, previous_order_id, order_id, order, messages)
        else:
            return PlaceOrderResponse(order_metadata, preview_id, order_id, order, messages)

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
    def _parse_preview_order_response(response, order_metadata: OrderMetadata, previous_order_id=None)-> PreviewOrderResponse:
        data = json.loads(response.text)
        preview_order_response = data["PreviewOrderResponse"]
        preview_ids: list[dict[str:str]] = preview_order_response["PreviewIds"]
        orders: list[dict] = preview_order_response["Order"]

        preview_id = preview_ids[0]["previewId"]
        order_dict = orders[0]

        estimated_total_amount: Amount = Amount.from_float(order_dict["estimatedTotalAmount"])
        estimated_commission: Amount = Amount.from_float(order_dict["estimatedCommission"])

        order = OrderConversionUtil.to_order_from_json(order_dict)
        order_preview: OrderPreview = OrderPreview(preview_id, order, estimated_total_amount, estimated_commission)

        # how to check if it replaces order
        if previous_order_id:
            return PreviewModifyOrderResponse(order_metadata, preview_id, previous_order_id, order_preview)
        else:
            return PreviewOrderResponse(order_metadata, preview_id, order_preview)

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
            order_detail = order["OrderDetail"][0]
            status: OrderStatus = OrderStatus[str(order_detail['status']).upper()]
            order_id = order["orderId"]

            placed_order: PlacedOrder = OrderConversionUtil.to_placed_order_from_json(order, account_id, order_id)

            if status == OrderStatus.EXECUTED:
                executed_order = OrderConversionUtil.to_executed_order_from_json(order)
                return_order_list.append(executed_order)
            else:
                return_order_list.append(placed_order)

        return return_order_list

    @staticmethod
    def _parse_get_order_response(response, account_id, order_id) -> GetOrderResponse:
        data = response.json()
        print(data)

        orders_response = data["OrdersResponse"]
        order = orders_response['Order'][0]

        placed_order: PlacedOrder = OrderConversionUtil.to_placed_order_from_json(order, account_id, order_id)

        if order["OrderDetail"][0]["status"] == OrderStatus.EXECUTED:
            executed_order = OrderConversionUtil.to_executed_order_from_json(order)
            return GetOrderResponse(executed_order)
        else:
            return GetOrderResponse(placed_order)

    @staticmethod
    def _build_preview_order_xml(order, order_type: OrderType, client_order_id: str)->str:
        orders_xml: list[str] = [OrderConversionUtil.build_order(order)]

        orders_str = "\n".join(orders_xml)
        return f"""<PreviewOrderRequest>
                       <orderType>{order_type.name}</orderType>
                       <clientOrderId>{client_order_id}</clientOrderId>
                       {orders_str}
                   </PreviewOrderRequest>"""

