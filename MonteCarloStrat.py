from PathGenerator import *
from EulerScheme import *
from VorCell import *
from LoadDataOpt import *
from Env import *
from progressBar import print_progress
import math as mt
import numpy as np


class MonteCarloStrat:
    """
    Perform a Monte Carlo simulation of an option price
    """
    def __init__(self, env):
        self._env = env

    def simulation(self, N, M):
        """
        M is the number of simulations
        """
        ans = 0

        data = LoadDataOpt(N)
        pg = PathGenerator(self._env, data)
        lst = VorCell.cartProd(pg.decomp)

        # Get the probabilities in each strat
        p = []
        count = 0
        for i in range(len(pg.decomp)):
            p.append(data.getProb(pg.decomp[i]))

        # Simulations
        prices = []
        for el in lst:
            print_progress(lst.index(el) + 1, len(lst), bar_length=20)
            # First compute the number of simulation in the strat
            pLoc = 1
            for i in range(len(el)):
                pLoc = pLoc * p[i][el[i]]
            count = count + round(M * pLoc)
            # Then simulate those observations
            for i in range(int(round(M * pLoc))):
                y = pg.randomPath(el)
                es = EulerScheme(self._env, y)
                price = self.priceOption(es.result())
                prices.append(price * mt.exp(-0.04))

        ans = np.mean(prices)
        sd = np.std(prices)
        ic1 = ans - 1.96 * sd / np.sqrt(M)
        ic2 = ans + 1.96 * sd / np.sqrt(M)

        print('Sd : ' + str(sd))
        print('confidance = [' + str(ic1) + ',' + str(ic2) + ']')
        return ans

    def priceOption(self, valSDE):
        price = max(valSDE - self._env.K, 0)
        return price

    # GETTERS, SETTERS AND PROPERTIES #

    def _get_env(self):
        return self._env

    def _set_env(self, env):
        self._env = env

    env = property(_get_env, _set_env)
