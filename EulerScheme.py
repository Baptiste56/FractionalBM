class EulerScheme:
    """
    Compute the result of an SDE using euler scheme
    """
    def __init__(self, x, W):
        self._x = x
        self._W = W
        self._b = 0
        self._sig = 1
        self._S0 = 100

    def result(self):
        ans = self._S0
        for i in range(len(self._x) - 1):
            ans = ans + self._b * (self._x[i + 1] - self._x[i]) +\
                self._sig * (self._W[i + 1] - self._W[i])
        return ans

    # GETTERS, SETTERS AND PROPERTIES #

    def _get_x(self):
        return self._x

    def _set_x(self, x):
        self._x = x

    def _get_W(self):
        return self._W

    def _set_W(self, W):
        self._W = W

    def _get_b(self):
        return self._b

    def _set_b(self, b):
        self._b = b

    def _get_sig(self):
        return self._sig

    def _set_sig(self, sig):
        self._sig = sig

    x = property(_get_x, _set_x)
    N = property(_get_W, _set_W)
    b = property(_get_b, _set_b)
    sig = property(_get_sig, _set_sig)
