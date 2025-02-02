import string
from random import choices


class OrderUtil:
    @staticmethod
    def generate_random_client_order_id():
        return "".join(choices(string.ascii_uppercase + string.digits, k=15))
