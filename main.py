from LoadDataOpt import *
from PathGenerator import *
from VorCell import *
from Env import *
import numpy as np
import matplotlib.pyplot as plt


x = np.linspace(0, 1, 501)
env = Env(x)
data = LoadDataOpt(20)

pg = PathGenerator(env, data)
lst = [3, 1]
y1 = pg.randomPath(lst)
y2 = pg.randomPath(lst)
y3 = pg.randomPath(lst)
y4 = pg.randomPath(lst)

cel = VorCell(env, data)
yDir = cel.vorCell([-0.6098, 0.799])

yVec = []
cel.sendAllCells(20, yVec)
for y in yVec:
    plt.plot(x, y, 'grey')

plt.plot(x, y1, 'red')
plt.plot(x, y2, 'brown')
plt.plot(x, y3, 'yellow')
plt.plot(x, y4, 'green')
plt.plot(x, yDir, 'blue')
plt.axis([0, 1, -3, 3])
plt.show()
