from pydantic import BaseModel

from common.finance.amount import Amount
from common.order.order import Order


class OrderPreview(BaseModel):
    preview_id: str
    order: Order
    total_order_value: Amount
    estimated_commission: Amount

    def as_preview_id_to_order(self)->(str, Order):
        return self.preview_id, self.order