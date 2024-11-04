DEFAULT_NUM_POSITIONS = 1000


class GetPortfolioRequest:
    def __init__(self, account_id: str, count=DEFAULT_NUM_POSITIONS):
        self.account_id: str = account_id
        self.count = count