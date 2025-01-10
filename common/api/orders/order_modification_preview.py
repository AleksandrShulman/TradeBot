from common.api.orders.order_preview import OrderPreview
from common.finance.amount import Amount
from common.order.order import Order

# TODO: Figure out if this is necessary of it this can be done with just tuples
# Pros: Having this is easier to maintain if items need to be added/removed
class OrderModificationPreview(OrderPreview):
    def __init__(self, order_id, preview_id, order: Order, total_order_value: Amount, estimated_commission: Amount):
        super().__init__(preview_id, order, total_order_value, estimated_commission)
        self.order_id = order_id
        self.preview_id = preview_id
        self.order = order