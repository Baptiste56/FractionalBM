from MonteCarloStrat import *
from Env import *
import numpy as np


x = np.linspace(0, 1, 6)
env = Env(x, K=120)
mc = MonteCarloStrat(env)
print(mc.simulation(10, 1000000))
