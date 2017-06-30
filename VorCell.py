import math as mt
import numpy as np
import itertools
from LoadDataOpt import *
from Env import *


class VorCell:
    """
    Definition of Voronoi Cell
    """

    def __init__(self, env, data):
        self._env = env
        self._data = data

    def eigVal(self, k, T):
        return mt.pow(T / (mt.pi * (k - 0.5)), 2)

    def eigVec(self, k, x, T):
        if isinstance(x, float):
            return self.eigVec2(k, x, T)
        else:
            ans = []
            for v in x:
                ans.append(mt.sqrt(2 / T) *
                           mt.sin(mt.pi * (k - 0.5) * (v / T)))
            return ans

    def eigVecPrim(self, k, x, T):
        if isinstance(x, float):
            return self.eigVecPrim2(k, x, T)
        else:
            ans = []
            for v in x:
                    ans.append(mt.sqrt(2 / T) * (mt.pi / T) * (k - 0.5) *
                               mt.cos(mt.pi * (k - 0.5) * (v / T)))
            return ans

    def eigVecPrim2(self, k, x, T):
        return mt.sqrt(2 / T) * (mt.pi / T) * (k - 0.5) *\
            mt.cos(mt.pi * (k - 0.5) * (x / T))

    def eigVec2(self, k, x, T):
        return mt.sqrt(2 / T) * mt.sin(mt.pi * (k - 0.5) * (x / T))

    def vorCell(self, lst):
        ans = np.multiply(lst[0] * mt.sqrt(self.eigVal(1, 1)),
                          self.eigVec(1, self._env.x, 1))
        for i in range(1, len(lst)):
            ans = np.add(ans, np.multiply(lst[i] *
                         mt.sqrt(self.eigVal(2, 1)),
                         self.eigVec(2, self._env.x, 1)))
        return ans

    def sendAllCells(self, N, finalList):
        data = LoadDataOpt(N)
        lstUniQuant = []
        for el in data.decomp:
            lstUniQuant.append(data.getUniQuant(el))
        lst = self.cartProd(data.decomp)
        ans = []
        for sublst in lst:
            ansTemp = []
            i = 0
            for el in sublst:
                ansTemp.append(lstUniQuant[i][el])
                i = i + 1
            ans.append(ansTemp)
        for el in ans:
            finalList.append(self.vorCell(el))
        return

    def cartProd(cls, lst):
        ans = []
        if(len(lst) == 1):
            ans = range(lst[0])
        else:
            for i in itertools.product(range(lst[0]), range(lst[1])):
                ans.append(list(i))

            for j in range(2, len(lst)):
                ansTemp = []
                for i in itertools.product(ans, range(lst[j])):
                    temp = list(i)
                    temp2 = temp[0][:]
                    temp2.append(temp[1])
                    ansTemp.append(temp2)
                ans = ansTemp[:]

        return ans

    # CLASS METHODS #
    cartProd = classmethod(cartProd)

    # GETTERS, SETTERS AND PROPERTIES #

    def _get_env(self):
        return self._env

    def _set_env(self, env):
        self._env = env

    def _get_data(self):
        return self._data

    def _set_data(self, data):
        self._data = data

    env = property(_get_env, _set_env)
    data = property(_get_data, _set_data)
