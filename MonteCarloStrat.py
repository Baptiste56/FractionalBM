from PathGenerator import *
from EulerScheme import *
from VanillaOption import *
from VorCell import *
from LoadDataOpt import *
from Env import *
from OptimAlloc import *
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
        N is the number of strata
        """
        ans = 0
        sd = 0

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
        tabHist = []

        # Two options : optim alloc or natural alloc
        # choice = "optim"
        choice = "optim"

        if(choice == "natural"):
            print_progress(0, len(lst), bar_length=20)
            for el in lst:
                # First compute the number of simulation in the strat
                pLoc = 1
                for i in range(len(el)):
                    pLoc = pLoc * p[i][el[i]]
                count = count + round(M * pLoc)
                # Then simulate those observations
                for i in range(int(round(M * pLoc))):
                    y = pg.randomPath(el)
                    tabHist.append(y[-1])
                    # es = EulerScheme(self._env, y)
                    es = VanillaOption(self._env, y[-1])
                    price = self.priceOption(es.result())
                    prices.append(price * mt.exp(-self._env.b))
                print_progress(lst.index(el) + 1, len(lst), bar_length=20)
            ans = np.mean(prices)
            sd = np.std(prices) / np.sqrt(M)
        else:  # Case optimal
            steps = 2
            print_progress(0, steps * len(lst), bar_length=20)
            count = 0
            p2 = []  # probability of each strata
            X = []
            for el in lst:
                pLoc = 1
                for i in range(len(el)):
                    pLoc = pLoc * p[i][el[i]]
                p2.append(pLoc)

            oa = OptimAlloc(p2, M, steps)
            m = oa.initAlloc()

            # First simulation
            for i in range(len(lst)):
                tmp = []
                # Simulate those observations
                for j in range(int(m[i])):
                    y = pg.randomPath(lst[i])
                    # es = EulerScheme(self._env, y)
                    es = VanillaOption(self._env, y[-1])
                    price = self.priceOption(es.result())
                    tmp.append(price * mt.exp(-self._env.b))
                X.append(tmp)
                count = count + 1
                print_progress(count, steps * len(lst), bar_length=20)
            # Next simulations
            for l in range(1, steps):
                m = oa.alloc(l, X)
                for i in range(len(lst)):
                    tmp = []
                    # Simulate those observations
                    for j in range(int(m[i])):
                        y = pg.randomPath(lst[i])
                        # es = EulerScheme(self._env, y)
                        es = VanillaOption(self._env, y[-1])
                        price = self.priceOption(es.result())
                        tmp.append(price * mt.exp(-self._env.b))
                    X[i] = X[i] + tmp
                    count = count + 1
                    print_progress(count, steps * len(lst), bar_length=20)
            meanStrat = []
            for i in range(len(X)):
                meanStrat.append(np.mean(X[i]))
            meanStrat = np.array(meanStrat)
            p2 = np.array(p2)
            ans = np.sum(meanStrat * p2)
            for i in range(len(X)):
                sd = sd + ((p2[i]**2) * (np.std(X[i])**2) / len(X[i]))
            sd = np.sqrt(sd)

        ic1 = ans - 1.96 * sd
        ic2 = ans + 1.96 * sd

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
