from MonteCarloStrat import *
from Env import *
import numpy as np


x = np.linspace(0, 1, 101)
env = Env(x)
mc = MonteCarloStrat(env)
print(mc.simulation(10, 1000))
