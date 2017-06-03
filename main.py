from VorCell import *
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0, 1, 0.01)
obj = VorCell(x)
yVec = []
obj.sendAllCells(20, yVec)
for y in yVec:
    plt.plot(x, y, 'black')
plt.show()
