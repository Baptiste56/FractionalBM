from LoadDataOpt import *
from VorCell import *
import random as rd
from scipy.stats import norm as no
import math as mt


class PathGenerator:
    """
    Generate a path for Gaussian Process with repect
    to a Voronoi cell.
    """
    def __init__(self, x, N):
        self._N = N
        self._x = x
        self.data = LoadDataOpt(N)
        self.decomp = self.data.decomp

    def randomPath(self, lst):
        n = len(self._x)
        d = len(self.decomp)
        y = []

        # GENERATE FIRST K-L OF THE PATH #
        for i in range(d):
            bor = LoadDataOpt.getEdges(self.decomp[i])
            u = rd.uniform(0, 1)
            a = no.ppf((no.cdf(bor[lst[i] + 1]) -
                        no.cdf(bor[lst[i]])) * u + no.cdf(bor[lst[i]]))
            a = a * mt.sqrt(VorCell.eigVal(i + 1, 1))
            y.append(a)

        # SIMULATE V (BROWNIAN MOTION) #
        V = [0]
        for i in range(n - 1):
            inc = rd.normalvariate(0, mt.sqrt(self._x[i + 1] - self._x[i]))
            V.append(V[i] + inc)
        V = np.matrix(V).T

        # SIMULATE G #
        # ---- Matrix definition ----
        h = 1.0 / n
        rYV = [n * [0] for i in range(d)]
        rVY = [n * [0] for i in range(d)]
        for i in range(d):
            lambdaI = VorCell.eigVal(i + 1, 1)
            eI = VorCell.eigVec(i + 1, self._x, 1)
            rVY[i] = eI[:]
            for j in range(n):
                if(j == 0):
                    rYV[i][j] = lambdaI *\
                        (VorCell.eigVecPrim(i + 1, self._x[0], 1) -
                                           ((eI[1] - eI[0]) / h))
                elif(j == n - 1):
                    rYV[i][j] = lambdaI *\
                        (((eI[n - 1] - eI[n - 2]) / h) -
                            VorCell.eigVecPrim(i + 1, self._x[n - 1], 1))
                else:
                    rYV[i][j] = lambdaI * (2 * eI[j] -
                                           eI[j - 1] - eI[j + 1]) / h
        rYV = np.matrix(rYV)
        rVY = np.matrix(rVY).T

        aYV = rYV * V

        covY = [d * [0] for i in range(d)]
        for i in range(d):
            covY[i][i] = VorCell.eigVal(i + 1, 1)
        covY = np.matrix(covY)

        covV = [n * [0] for i in range(n)]
        for i in range(n):
            for j in range(n):
                covV[i][j] = min(self._x[i], self._x[j])
        covV = np.matrix(covV)

        K = covY - rYV * covV * rYV.T

        G = np.random.multivariate_normal(np.squeeze(np.asarray(aYV.T)),
                                          np.asarray(K))
        G = np.matrix(G)

        Z = V - rVY * G.T
        ans = rVY * np.matrix(y).T + Z

        return np.squeeze(np.asarray(ans.T))

    # GETTERS, SETTERS AND PROPERTIES #

    def _get_x(self):
        return self._x

    def _set_x(self, x):
        self._x = x

    def _get_N(self):
        return self._N

    def _set_N(self, N):
        self._N = N

    x = property(_get_x, _set_x)
    N = property(_get_N, _set_N)
