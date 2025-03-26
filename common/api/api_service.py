from abc import ABC

from common.exchange.connector import Connector


class ApiService(ABC):
    def __init__(self, connector: Connector):
        self.connector = connector