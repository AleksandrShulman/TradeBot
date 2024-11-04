from enum import Enum


class OptionType(Enum):
    # make this an enum for PUT or CALL
    PUT = 0
    CALL = 1

    @staticmethod
    def from_str(input:str):
        if input.lower() == "put":
            return OptionType.PUT
        elif input.lower() == "call":
            return OptionType.CALL
        else:
            raise Exception(f"Could not map {input} to option type")
