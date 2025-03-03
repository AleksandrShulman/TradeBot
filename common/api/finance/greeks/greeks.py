class Greeks:
    def __init__(self, delta: float, gamma, theta, vega, rho, iv, current_value: bool):
        self.delta = delta
        self.gamma = gamma
        self.theta = theta
        self.vega = vega
        self.rho = rho
        self.iv = iv
        self.current_value = current_value