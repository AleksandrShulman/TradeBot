from common.finance.amount import Amount
from common.order.order import Order


class OrderPreview:
    def __init__(self, preview_id:str, order: Order, total_order_value: Amount, estimated_commission: Amount):
        self.preview_id: str = preview_id
        self.order: Order = order
        self.total_order_value: Amount = total_order_value
        self.estimated_commission: Amount = estimated_commission

    def as_preview_id_to_order(self)->(str, Order):
        return self.preview_id, self.order