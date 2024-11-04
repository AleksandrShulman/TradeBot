from enum import Enum

EUROPEAN_OPTIONS_SET = {"VIX", "VIXW", "SPX", "XSP"}


class OptionStyle(Enum):
    # make this an enum for American or European
    AMERICAN = 0
    EUROPEAN = 1

    @staticmethod
    def from_ticker(ticker):
        if ticker in EUROPEAN_OPTIONS_SET:
            return OptionStyle.EUROPEAN
        return OptionStyle.AMERICAN

    @staticmethod
    def from_expiry_type(expiry_type: str):
        if not expiry_type:
            raise Exception(f"Could not parse expiry type: {expiry_type}")
        if expiry_type.lower() == "american":
            return OptionStyle.AMERICAN
        if expiry_type.lower() == "european":
            return OptionStyle.EUROPEAN
        else:
            raise Exception(f"Could not parse expiry type: {expiry_type}")
