from LoadDataOpt import *
from VorCell import *
import random as rd
from scipy.stats import norm as no
import math as mt
import numpy as np


class PathGenerator:
    """
    Generate a path for Gaussian Process with repect
    to a Voronoi cell (pass throught lst).
    The number of strat is predefined with data.
    """
    def __init__(self, env, data):
        self._env = env
        self._data = data
        self._edges = []
        self._vc = VorCell(env, data)

        # 2 next variables redefined for convinience,
        # please do not change the value here.
        self._x = self._env.x
        self.decomp = self._data.decomp

        n = len(self._x)
        d = len(self.decomp)
        self._rYV = [n * [0] for i in range(d)]
        self._rVY = [n * [0] for i in range(d)]
        self._covY = [d * [0] for i in range(d)]
        self._covV = [n * [0] for i in range(n)]
        self.initiateMatrices()

    def initiateMatrices(self):
        n = len(self._x)
        d = len(self.decomp)
        h = 1.0 / (n - 1)
        for i in range(len(self.decomp)):
            self._edges.append(self._data.getEdges(self.decomp[i]))

        for i in range(n):
            for j in range(n):
                self._covV[i][j] = min(self._x[i], self._x[j])
        self._covV = np.matrix(self._covV)

        for i in range(d):
            lambdaI = self._vc.eigVal(i + 1, 1)
            eI = self._vc.eigVec(i + 1, self._x, 1)
            self._rVY[i] = eI[:]
            for j in range(n):
                if(j == 0):
                    self._rYV[i][j] = lambdaI *\
                        (self._vc.eigVecPrim(i + 1, self._x[0], 1) -
                         ((eI[1] - eI[0]) / h))
                elif(j == n - 1):
                    self._rYV[i][j] = lambdaI *\
                        (((eI[n - 1] - eI[n - 2]) / h) -
                         self._vc.eigVecPrim(i + 1, self._x[n - 1], 1))
                else:
                    self._rYV[i][j] = lambdaI * (2 * eI[j] -
                                                 eI[j - 1] - eI[j + 1]) / h
        self._rYV = np.matrix(self._rYV)
        self._rVY = np.matrix(self._rVY).T

        for i in range(d):
            self._covY[i][i] = self._vc.eigVal(i + 1, 1)
        self._covY = np.matrix(self._covY)
        return

    def randomPath(self, lst):
        n = len(self._x)
        d = len(self.decomp)
        y = []

        # GENERATE FIRST K-L OF THE PATH #
        for i in range(d):
            u = rd.uniform(0, 1)
            a = no.ppf((no.cdf(self._edges[i][lst[i] + 1]) -
                        no.cdf(self._edges[i][lst[i]])) * u +
                       no.cdf(self._edges[i][lst[i]]))
            a = a * mt.sqrt(self._vc.eigVal(i + 1, 1))
            y.append(a)

        # SIMULATE V (BROWNIAN MOTION) #
        V = [0]
        for i in range(n - 1):
            inc = rd.normalvariate(0, np.sqrt(self._x[i + 1] - self._x[i]))
            V.append(V[i] + inc)
        V = np.matrix(V).T

        # SIMULATE G #
        # ---- Matrix definition ----

        aYV = self._rYV * V

        Msym = self._rYV * self._covV * self._rYV.T
        Msym = np.squeeze(np.asarray(Msym))
        for i in range(len(Msym)):
            for j in range(0, len(Msym)):
                Msym[i][j] = Msym[j][i]

        K = self._covY - Msym

        G = np.random.multivariate_normal(np.squeeze(np.asarray(aYV.T)),
                                          np.asarray(K))
        G = np.matrix(G)

        Z = V - self._rVY * G.T
        ans = self._rVY * np.matrix(y).T + Z

        return np.squeeze(np.asarray(ans.T))

    # GETTERS, SETTERS AND PROPERTIES #

    def _get_edges(self):
        return self._edges

    def _set_edges(self, edges):
        self._edges = edges

    def _get_rYV(self):
        return self._rYV

    def _set_rYV(self, rYV):
        self._rYV = rYV

    def _get_rVY(self):
        return self._rVY

    def _set_rVY(self, rVY):
        self._rVY = rVY

    def _get_covY(self):
        return self._covY

    def _set_covY(self, covY):
        self._covY = covY

    def _get_covV(self):
        return self._covV

    def _set_covV(self, covV):
        self._covV = covV

    edges = property(_get_edges, _set_edges)
    rYV = property(_get_rYV, _set_rYV)
    rVY = property(_get_rVY, _set_rVY)
    covY = property(_get_covY, _set_covY)
    covV = property(_get_covV, _set_covV)
