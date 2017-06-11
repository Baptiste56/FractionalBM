from PathGenerator import *
from EulerScheme import *
from VorCell import *
from LoadDataOpt import *


class MonteCarloStrat:
    """
    Perform a Monte Carlo simulation of an option price
    """
    def __init__(self, x):
        self._x = x

    def simulation(self, N, M):
        # M is the number of simulations
        ans = 0
        pg = PathGenerator(self._x, N)
        lst = VorCell.cartProd(pg.decomp)

        # Get the probabilities in each strat
        p = []
        count = 0
        for i in range(len(pg.decomp)):
            p.append(LoadDataOpt.getProb(pg.decomp[i]))
        for el in lst:
            pLoc = 1
            for i in range(len(el)):
                pLoc = pLoc * p[i][el[i]]
            count = count + round(M * pLoc)
            for i in range(int(round(M * pLoc))):
                y = pg.randomPath(el)
                es = EulerScheme(self._x, y)
                ans = ans + (es.result() / M)
        print(count)
        ans = ans * (M / count)
        return ans
