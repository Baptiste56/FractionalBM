import os
import re


class LoadDataOpt:
    """
    Load data of optimal quantization from the
    website http://www.quantize.maths-fi.com/
    """
    def __init__(self, N):
        self._decomp = []
        self._N = N
        self.getDecomp()

    def getDecomp(self):
        os.chdir("/Users/portenardbaptiste/Python")
        dataFile = open("RECORD_QF.TXT", "r")
        for i in range(1, self._N):
            dataFile.readline()
        data = dataFile.readline()
        dataFile.close()
        data = data.split()
        for i in range(0, 4):
            del data[0]

        lst = [int(x) for x in data]
        self._decomp = lst

    def getUniQuant(self, k):
        os.chdir("/Users/portenardbaptiste/Python/one_dim_1_1000")
        dataFile = open("{0}_1_nopti".format(k), "r")
        data = dataFile.read()
        dataFile.close()

        lst = [float(x) for x in re.split("	|\n", data)]

        val = []
        for i in range(0, k):
            val.append(lst[i * 4 + 1])
        return val

    def getEdges(self, k):
        ans = []
        val = self.getUniQuant(k)
        if(len(val) == 1):
            ans.append(float('-inf'))
            ans.append(float('inf'))
        else:
            ans.append(float('-inf'))
            for i in range(0, len(val) - 1):
                ans.append((val[i] + val[i + 1]) / 2)
            ans.append(float('inf'))
        return ans

    def getProb(self, k):
        os.chdir("/Users/portenardbaptiste/Python/one_dim_1_1000")
        dataFile = open("{0}_1_nopti".format(k), "r")
        data = dataFile.read()
        dataFile.close()

        lst = [float(x) for x in re.split(" |\n|\t", data)]

        val = []
        for i in range(0, k):
            val.append(lst[i * 4])
        return val

    # GETTERS, SETTERS AND PROPERTIES #

    def _get_decomp(self):
        return self._decomp

    def _set_decomp(self, decomp):
        self._decomp = decomp

    def _get_N(self):
        return self._N

    def _set_N(self, N):
        self._N = N

    decomp = property(_get_decomp, _set_decomp)
    N = property(_get_N, _set_N)
