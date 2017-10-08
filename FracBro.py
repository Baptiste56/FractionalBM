import os
import re


class FracBro:
    """
    Fractional Brownian motion
    """

    def __init__(self):
        self._eigVal = []
        self._eigVec = []
        self.importData()

    def importData(self):
        H = 0.8
        os.chdir("/Users/portenardbaptiste/Python/fracBroVorCell")
        file = open("EigValTest_{0}.txt".format(H), "r")
        # file = open("EigValTest.txt", "r")
        data = file.read()
        lst = re.split(" |\n|\t", data)
        lst.pop()
        self._eigVal = [float(x) for x in lst]
        file.close()
        for i in range(3):  # Change the numbers according to dim
            temp = []
            file = open("EigVec{0}Test_{1}.txt".format(i + 1, H), "r")
            # file = open("EigVec{0}Test.txt".format(i + 1), "r")
            data = file.read()
            lst = re.split(" |\n|\t", data)
            lst.pop()
            temp = [float(x) for x in lst]
            self._eigVec.append(temp[:])
            file.close()
