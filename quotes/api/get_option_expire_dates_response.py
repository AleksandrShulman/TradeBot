from datetime import datetime


class GetOptionExpireDatesResponse:
    def __init__(self, expire_dates: list[datetime]):
        # Perhaps a date will also be required
        self.expire_dates = expire_dates
