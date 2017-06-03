import os
import re


class LoadDataOpt:
    """
    Load data of optimal quantization from the
    website http://www.quantize.maths-fi.com/
    """
    def __init__(self, N):
        self.decomp = []
        self.N = N
        self.getDecomp()

    def getDecomp(self):
        dataFile = open("RECORD_QF.TXT", "r")
        for i in range(1, self.N):
            dataFile.readline()
        data = dataFile.readline()
        dataFile.close()
        data = data.split()
        for i in range(0, 4):
            del data[0]

        lst = [int(x) for x in data]
        self.decomp = lst

    def getUniQuant(cls, k):
        os.chdir("/Users/portenardbaptiste/Python/one_dim_1_1000")
        dataFile = open("{0}_1_nopti".format(k), "r")
        data = dataFile.read()
        dataFile.close()

        lst = [float(x) for x in re.split("	|\n", data)]

        val = []
        for i in range(0, k):
            val.append(lst[i * 4 + 1])
        return val

    # CLASS METHODS #

    getUniQuant = classmethod(getUniQuant)
