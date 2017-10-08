import math as mt


class VanillaOption:
    """
    Perform a Monte Carlo simulation of an option price
    """
    def __init__(self, env, W):
        self._env = env
        self._W = W

    def result(self):
        term1 = self._env.b - ((self._env.sig**2) / 2)
        term2 = self._env.sig * self._W
        ans = mt.exp((term1 * self._env.T) + term2)
        ans = self._env.S0 * ans
        return ans
