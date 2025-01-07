from common.api.response import Response
from common.finance.amount import Amount

class OrderPreview:
    def __init__(self, preview_id:str, total_order_value: Amount, estimated_commission: Amount):
        self.preview_id: str = preview_id
        self.total_order_value: Amount = total_order_value
        self.estimated_commission: Amount = estimated_commission

class PreviewOrdersResponse(Response):
    def __init__(self, order_previews: list[OrderPreview]):
        self.order_previews = order_previews
