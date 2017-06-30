

class Env:
    """
    Definition of the environment
    """
    def __init__(self, x, b=0.04, sig=0.25, T=1., S0=100., K=100.):
        self._x = x
        self._b = b
        self._sig = sig
        self._T = T
        self._S0 = S0
        self._K = K

    def show(self):
        print('length x = ' + str(len(self._x)))
        print('b = ' + str(self._b))
        print('sig = ' + str(self._sig))
        print('T = ' + str(self._T))
        print('S0 = ' + str(self._S0))
        print('K = ' + str(self._K))
        return

    # GETTERS, SETTERS AND PROPERTIES #

    def _get_x(self):
        return self._x

    def _set_x(self, x):
        self._x = x

    def _get_b(self):
        return self._b

    def _set_b(self, b):
        self._b = b

    def _get_sig(self):
        return self._sig

    def _set_sig(self, sig):
        self._sig = sig

    def _get_T(self):
        return self._T

    def _set_T(self, T):
        self._T = T

    def _get_S0(self):
        return self._S0

    def _set_S0(self, S0):
        self._S0 = S0

    def _get_K(self):
        return self._K

    def _set_K(self, K):
        self._K = K

    x = property(_get_x, _set_x)
    b = property(_get_b, _set_b)
    sig = property(_get_sig, _set_sig)
    T = property(_get_T, _set_T)
    S0 = property(_get_S0, _set_S0)
    K = property(_get_K, _set_K)
