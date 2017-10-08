import numpy as np
import math as mt
import os
import matplotlib.pyplot as plt


def trapeze(x, k):
    H = 0.8
    He = 2 * H
    N = len(x)
    h = 1. / (N - 1)
    # K is the covariance matrix
    K = [N * [0] for i in range(N)]
    for i in range(N):
        for j in range(N):
            # K[i][j] = min(x[i], x[j])
            K[i][j] = 0.5 * (x[i]**He + x[j]**He - abs(x[j] - x[i])**He)
    K = np.matrix(K)

    D = [N * [0] for i in range(N)]
    D[0][0] = h / 2
    D[N - 1][N - 1] = h / 2
    for i in range(1, N - 1):
        D[i][i] = h
    D2 = np.matrix(np.sqrt(D))

    w, _ = np.linalg.eigh(D2 * K * D2)
    return w[-k]


def trapeze2(x, k):
    H = 0.8
    He = 2 * H
    N = len(x)
    h = 1. / (N - 1)
    K = [N * [0] for i in range(N)]
    for i in range(N):
        for j in range(N):
            # K[i][j] = min(x[i], x[j])
            K[i][j] = 0.5 * (x[i]**He + x[j]**He - abs(x[j] - x[i])**He)
    K = np.matrix(K)

    D = [N * [0] for i in range(N)]
    D[0][0] = h / 2
    D[N - 1][N - 1] = h / 2
    for i in range(1, N - 1):
        D[i][i] = h
    D2 = np.matrix(np.sqrt(D))

    Dinv = [N * [0] for i in range(N)]
    Dinv[0][0] = np.sqrt(2. / h)
    Dinv[N - 1][N - 1] = np.sqrt(2. / h)
    for i in range(1, N - 1):
        Dinv[i][i] = np.sqrt(1. / h)
    Dinv = np.sqrt(Dinv)

    _, v = np.linalg.eigh(D2 * K * D2)
    v = v[:, -k].T.tolist()
    v = np.squeeze(v)
    v = Dinv.dot(v)
    v = v / (1. / np.sqrt(10))
    v[-1] = v[-1] / 0.840896415254  # Don't know why
    return v


def eigVal(l):
    lbda = (1 / ((l - 0.5) * np.pi))**2
    print('theoric : ' + str(lbda))

    U = []
    k = []
    x = np.linspace(0, 1, 26)
    U.append(trapeze(x, l))
    k.append(25)
    x = np.linspace(0, 1, 51)
    U.append(trapeze(x, l))
    k.append(50)
    x = np.linspace(0, 1, 101)
    U.append(trapeze(x, l))
    k.append(100)
    val = Romberg3(U, k)
    print('experimental : ' + str(val))
    print('dif : ' + str(val - lbda))
    return val


def weight(l, r):
    H = 0.8
    alp = (1. / (2 * H)) - 1
    wl = (alp + 1) * (l ** (alp + 2)) + (r ** (alp + 2)) -\
         (alp + 2) * (l ** (alp + 1)) * r
    wl /= (2 * H * (alp + 1) * (alp + 2) * (r - l))
    wr = (alp + 1) * (r ** (alp + 2)) + (l ** (alp + 2)) -\
         (alp + 2) * (r ** (alp + 1)) * l
    wr /= (2 * H * (alp + 1) * (alp + 2) * (r - l))
    return wl, wr


def testInt(a, b, l, r):
    wl, wr = weight(l, r)
    return wl * (a * l + b) + wr * (a * r + b)


def testIntTheo(a, b, l, r):
    H = 0.3
    alp = (1. / (2 * H)) - 1
    ans = (1. / (2 * H)) * (a * intPow(alp + 1, l, r) + b * intPow(alp, l, r))
    return ans


def intPow(a, l, r):
    return (1. / (a + 1)) * (r**(a + 1) - l**(a + 1))


def trapeze3(x, k):
    H = 0.8
    He = 2 * H
    N = len(x)
    x2 = x**He  # Change of variable
    # K is the covariance matrix
    K = [N * [0] for i in range(N)]
    for i in range(N):
        for j in range(N):
            # K[i][j] = min(x[i], x[j])
            K[i][j] = 0.5 * (x[i]**He + x[j]**He - abs(x[j] - x[i])**He)
    K = np.matrix(K)

    D = [N * [0] for i in range(N)]
    D[0][0], D[1][1] = weight(x2[0], x2[1])
    for i in range(2, N):
        temp, D[i][i] = weight(x2[i - 1], x2[i])
        D[i - 1][i - 1] += temp
    D2 = np.matrix(np.sqrt(D))

    R = []
    for i in range(N):
        R.append(0.5 * (((1 - x[i]**(He + 1)) / (He + 1)) +
                 x[i]**He - ((1 - x[i])**(He + 1) / (He + 1))))

    temp = []
    for i in range(N):
        temp.append(D[i][i])
    temp = np.matrix(temp)

    Dl = [N * [0] for i in range(N)]
    for i in range(N):
        temp2 = np.matrix(K[i][:]).transpose()
        temp2 = temp * temp2
        Dl[i][i] = R[i] - float(temp2)
    Dl = np.matrix(Dl)

    w, _ = np.linalg.eigh((D2 * K * D2) + Dl)
    return w[-k]


def trapeze4(x, k):
    H = 0.8
    He = 2 * H
    N = len(x)
    x2 = x**He  # Change of variable
    # K is the covariance matrix
    K = [N * [0] for i in range(N)]
    for i in range(N):
        for j in range(N):
            # K[i][j] = min(x[i], x[j])
            K[i][j] = 0.5 * (x[i]**He + x[j]**He - abs(x[j] - x[i])**He)
    K = np.matrix(K)

    D = [N * [0] for i in range(N)]
    D[0][0], D[1][1] = weight(x2[0], x2[1])
    for i in range(2, N):
        temp, D[i][i] = weight(x2[i - 1], x2[i])
        D[i - 1][i - 1] += temp
    D2 = np.matrix(np.sqrt(D))

    Dinv = [N * [0] for i in range(N)]
    for i in range(N):
        Dinv[i][i] = 1. / np.sqrt(D[i][i])
    Dinv = np.sqrt(Dinv)

    R = []
    for i in range(N):
        R.append(0.5 * (((1 - x[i]**(He + 1)) / (He + 1)) +
                 x[i]**He - ((1 - x[i])**(He + 1) / (He + 1))))

    temp = []
    for i in range(N):
        temp.append(D[i][i])
    temp = np.matrix(temp)

    Dl = [N * [0] for i in range(N)]
    for i in range(N):
        temp2 = np.matrix(K[i][:]).transpose()
        temp2 = temp * temp2
        Dl[i][i] = R[i] - float(temp2)
    Dl = np.matrix(Dl)

    _, v = np.linalg.eigh((D2 * K * D2) + Dl)
    v = v[:, -k].T.tolist()
    v = np.squeeze(v)
    v = Dinv.dot(v)
    v = v / (1. / np.sqrt(10))
    v[-1] = v[-1] / 0.840896415254  # Don't know why
    return v


def Romberg3(U, k):
    val = U[0] * k[0]**4 * (k[2]**2 - k[1]**2)
    val = val + U[1] * k[1]**4 * (k[0]**2 - k[2]**2)
    val = val + U[2] * k[2]**4 * (k[1]**2 - k[0]**2)
    den = (k[2]**2 - k[1]**2) *\
        (k[2]**2 * k[1]**2 + k[0]**4 - k[2]**2 * k[0]**2 - k[1]**2 * k[0]**2)
    val = val / den
    return val


def writeEigVal(k):
    H = 0.8
    os.chdir("/Users/portenardbaptiste/Python/fracBroVorCell")
    file = open("EigValTest_{0}.txt".format(H), "w")
    for i in range(k):
        file.write(str(eigVal(i + 1)) + '\n')
    file.close()


def writeEigVec(k):
    os.chdir("/Users/portenardbaptiste/Python/fracBroVorCell")
    file = open("EigVec{0}Test.txt".format(k), "w")
    x = np.linspace(0, 1, 101)
    y = trapeze2(x, k)
    for i in range(len(y)):
        file.write(str(y[i]) + '\n')
    file.write('1')  # Avoid reading issues
    file.close()


def writeEigVal2(k):
    H = 0.8
    os.chdir("/Users/portenardbaptiste/Python/fracBroVorCell")
    file = open("EigValTest_{0}.txt".format(H), "w")
    x = np.linspace(0, 1, 101)
    for i in range(k):
        file.write(str(trapeze3(x, i + 1)) + '\n')
    file.close()


def writeEigVec2(k):
    H = 0.8
    os.chdir("/Users/portenardbaptiste/Python/fracBroVorCell")
    file = open("EigVec{0}Test_{1}.txt".format(k, H), "w")
    x = np.linspace(0, 1, 101)
    y = trapeze4(x, k)
    for i in range(len(y)):
        file.write(str(y[i]) + '\n')
    file.write('1')  # Avoid reading issues
    file.close()


def eigVecTest(k):
    x = np.linspace(0, 1, 101)
    y = trapeze2(x, k)
    y2 = []
    for i in range(len(x)):
        y2.append(np.sqrt(2) * np.sin(np.pi * (k - 0.5) * x[i]))
        print(y[i] / y2[i])


# eigVecTest(1)
# writeEigVal2(5)
writeEigVec2(1)
writeEigVec2(2)
writeEigVec2(3)
