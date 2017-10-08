import numpy as np


class OptimAlloc:
    """
    Optimal allocation for strata in variance reduction
    """
    def __init__(self, p, M, steps):
        self._I = len(p)
        self._sig = self._I * [0]  # deviation of each Vor Cell
        self._p = p  # weight of Vor cells
        self._M = M - (M % steps)  # Total number of simulation
        self._N = M / steps  # Simulation during one step

    def initAlloc(self):
        # X is a 2 dimensional array and represents the data in each stata
        m = []
        for i in range(self._I):
            m.append(self._p[i] * (self._N - self._I))
        m = sysSampling(m)
        return m

    def alloc(self, k, X):
        # X is a 2 dimensional array and represents the data in each stata
        # X[i] array of functional data in strata i
        m = []
        for i in range(self._I):
            self._sig[i] = np.mean(np.power(X[i], 2)) - np.mean(X[i])**2
            self._sig[i] = np.sqrt(self._sig[i])
        for i in range(self._I):
            pTmp = np.array(self._p)
            sigTmp = np.array(self._sig)
            m.append(self._p[i] * self._sig[i] *
                     (self._N - self._I) / np.sum(pTmp * sigTmp))
        m = sysSampling(m)
        return m


def sysSampling(m):
    # We add the +1 in the answer
    ans = []
    for i in range(len(m)):
        tmp1 = np.floor(np.sum(m[0:i + 1]))
        if(i == 0):
            tmp2 = 0
        else:
            tmp2 = np.floor(np.sum(m[0:i]))
        ans.append(tmp1 - tmp2 + 1)
    return ans
