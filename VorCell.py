import math as mt
import numpy as np
import itertools
from LoadDataOpt import *


class VorCell:
    """
    Definition of Voronoi Cell
    """

    def __init__(self, x):
        self.T = 1
        self._x = x

    def eigVal(cls, k, T):
        return mt.pow(T / (mt.pi * (k - 0.5)), 2)

    def eigVec(cls, k, x, T):
        if isinstance(x, float):
            return VorCell.eigVec2(k, x, T)
        else:
            ans = []
            for v in x:
                ans.append(mt.sqrt(2 / T) *
                           mt.sin(mt.pi * (k - 0.5) * (v / T)))
            return ans

    def eigVecPrim(cls, k, x, T):
        if isinstance(x, float):
            return VorCell.eigVecPrim2(k, x, T)
        else:
            ans = []
            for v in x:
                    ans.append(mt.sqrt(2 / T) * (mt.pi / T) * (k - 0.5) *
                               mt.cos(mt.pi * (k - 0.5) * (v / T)))
            return ans

    def eigVecPrim2(cls, k, x, T):
        return mt.sqrt(2 / T) * (mt.pi / T) * (k - 0.5) *\
            mt.cos(mt.pi * (k - 0.5) * (x / T))

    def eigVec2(cls, k, x, T):
        return mt.sqrt(2 / T) * mt.sin(mt.pi * (k - 0.5) * (x / T))

    def vorCell(self, lst):
        ans = np.multiply(lst[0] * mt.sqrt(VorCell.eigVal(1, 1)),
                          VorCell.eigVec(1, self._x, 1))
        for i in range(1, len(lst)):
            ans = np.add(ans, np.multiply(lst[i] *
                         mt.sqrt(VorCell.eigVal(2, 1)),
                         VorCell.eigVec(2, self._x, 1)))
        return ans

    def sendAllCells(self, N, finalList):
        data = LoadDataOpt(N)
        lstUniQuant = []
        for el in data.decomp:
            lstUniQuant.append(LoadDataOpt.getUniQuant(el))
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

    def cartProd(self, lst):
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
    eigVal = classmethod(eigVal)
    eigVec = classmethod(eigVec)
    eigVec2 = classmethod(eigVec2)
    eigVecPrim = classmethod(eigVecPrim)
    eigVecPrim2 = classmethod(eigVecPrim2)

    # GETTERS, SETTERS AND PROPERTIES #

    def _get_x(self):
        return self._x

    def _set_x(self, x):
        self._x = x

    x = property(_get_x, _set_x)
