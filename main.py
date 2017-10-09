from LoadDataOpt import *
from PathGenerator import *
from VorCell import *
from Env import *
import numpy as np
import matplotlib.pyplot as plt

NVorCell = 20

x = np.linspace(0, 1, 100)
env = Env(x)
data = LoadDataOpt(NVorCell)

# pg = PathGenerator(env, data)
# lst = [3, 1]
# y1 = pg.randomPath(lst)
# y2 = pg.randomPath(lst)
# y3 = pg.randomPath(lst)
# y4 = pg.randomPath(lst)

cel = VorCell(env, data)
# yDir = cel.vorCell([-0.6098, 0.799])

# yVec = []
# cel.sendAllCells(20, yVec)
# for y in yVec:
#     plt.plot(x, y, 'grey')

yVec = []
cel.sendAllCellsFrac(NVorCell, yVec)
for y in yVec:
    plt.plot(x, y, 'grey', lw=0.6)

# plt.plot(x, y1, 'red', lw=0.6)
# plt.plot(x, y2, 'brown', lw=0.6)
# plt.plot(x, y3, 'yellow', lw=0.6)
# plt.plot(x, y4, 'green', lw=0.6)
# plt.plot(x, yDir, 'blue')
plt.axis([0, 1, -2.7, 2.7])
plt.show()
