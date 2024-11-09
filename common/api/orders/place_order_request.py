from common.api.request import Request


class PlaceOrderRequest(Request):
    def __init__(self, order_id):
        self.order_id = order_id
