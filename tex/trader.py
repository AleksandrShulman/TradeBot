from abc import ABC


class Trader(ABC):
    def get_all_open_trades(self):
        pass

    def get_all_open_trades_for_symbol(self):
        pass

    def get_options_chain(self):
        pass

    def get_option_details(self):
        pass

