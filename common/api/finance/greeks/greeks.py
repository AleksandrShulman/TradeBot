from pydantic import BaseModel

from common.finance.price import Price


class Greeks(BaseModel):
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float
    iv: float
    current_value: Price