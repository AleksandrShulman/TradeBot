from abc import ABC

from common.exchange.connector import Connector


class OrderService(ABC):
    def __init__(self, connector: Connector):
        self.connector = connector
    pass