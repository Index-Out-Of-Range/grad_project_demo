import numpy
from django.core.cache import cache


def L21_CMNMF_LF(MaxIter, A1, A2, G, P1, P2, M, Y1, Y2, alpha, beta, gamma, miu, rou, process_key):
    # L为目标函数值
    D1 = numpy.diag(numpy.sum(M, axis=1))
    D2 = numpy.diag(numpy.sum(M, axis=0))
    # print(numpy.shape(D1))
    # print(numpy.shape(D2))
    E1 = numpy.zeros(numpy.shape(A1))
    E2 = numpy.zeros(numpy.shape(A2))
    Lambda1 = numpy.zeros(numpy.shape(A1))
    Lambda2 = numpy.zeros(numpy.shape(A2))
    L = numpy.zeros((MaxIter * 5, 2))
    # print(numpy.shape(E1))
    # print(E1)
    (L[0][0], L[0][1]) = objective(alpha, beta, gamma, miu, A1, A2, G, P1, P2, M, Y1, Y2, E1, E2, Lambda1, Lambda2)
    # print('L: ', L)
    t = 1
    for j in range(1, MaxIter + 1):
        print('Iter=' + str(j))
        print('process_key: ' + str(process_key))
        cache.set(process_key, j - 1)
        print('cache.get(process_key): ' + str(cache.get(process_key)))

        # update E1
        B = Y1 * (A1 - numpy.dot(G, P1)) + (1 / miu) * Lambda1
        # print('numpy.size(E1, 0): ', numpy.size(E1, 0))
        for row in range(numpy.size(E1, 0)):
            if numpy.linalg.norm(B[row]) >= 1 / miu:
                E1[row] = (1 - 1 / (miu * numpy.linalg.norm(B[row]))) * B[row]
            else:
                E1[row] = 0
        # update E2
        B = Y2 * (A2 - numpy.dot(G, P2)) + (1 / miu) * Lambda2
        for row in range(numpy.size(E2, 0)):
            if numpy.linalg.norm(B[row]) >= alpha / miu:
                E2[row] = (1 - alpha / (miu * numpy.linalg.norm(B[row]))) * B[row]
            else:
                E2[row] = 0
        # update G
        B = (Y1 * (E1 - (1 / miu) * Lambda1)).dot(P1.transpose()) + alpha * (Y2 * (E2 - (1 / miu) * Lambda2)).dot(
            P2.transpose())
        B_plus = (numpy.abs(B) + B) / 2
        B_minus = (numpy.abs(B) - B) / 2
        Delta_plus = (Y1 * (numpy.dot(G, P1))).dot(P1.transpose()) + alpha * (Y2 * (numpy.dot(G, P2))).dot(
            P2.transpose()) + gamma * G + B_plus
        Delta_minus = (Y1 * A1).dot(P1.transpose()) + alpha * ((Y2 * A2).dot(P2.transpose())) + B_minus
        G = G * (Delta_minus / Delta_plus)
        G[numpy.isnan(G)] = 0
        G[numpy.isinf(G)] = 0

        # update P1
        B = miu * (G.transpose()).dot((Y1 * (E1 - (1 / miu) * Lambda1)))
        B_plus = (numpy.abs(B) + B) / 2
        B_minus = (numpy.abs(B) - B) / 2
        Delta_plus = miu * (G.transpose()).dot(Y1 * (G.dot(P1))) + 2 * beta * P1.dot(D1) + 2 * gamma * P1 + B_plus
        Delta_minus = miu * (G.transpose()).dot(Y1 * A1) + 2 * beta * P2.dot(M.transpose()) + B_minus
        P1 = P1 * (Delta_minus / Delta_plus)
        P1[numpy.isnan(P1)] = 0
        P1[numpy.isinf(P1)] = 0

        # update P2
        B = miu * (G.transpose()).dot((Y2 * (E2 - (1 / miu) * Lambda2)))
        B_plus = (numpy.abs(B) + B) / 2
        B_minus = (numpy.abs(B) - B) / 2
        Delta_plus = miu * (G.transpose()).dot(Y2 * (G.dot(P2))) + 2 * beta * P2.dot(D2) + 2 * gamma * P2 + B_plus
        Delta_minus = miu * (G.transpose()).dot(Y2 * A2) + 2 * beta * numpy.dot(P1, M) + B_minus
        P2 = P2 * (Delta_minus / Delta_plus)
        P2[numpy.isnan(P2)] = 0
        P2[numpy.isinf(P2)] = 0

        # update ALM parameters
        Lambda1 = Lambda1 + miu * (Y1 * (A1 - numpy.dot(G, P1)) - E1)
        Lambda2 = Lambda2 + miu * (Y2 * (A2 - numpy.dot(G, P2)) - E2)
        miu = numpy.min((pow(10, 1000), miu * rou))

    # print('L: ', L)
    # print('G: ', G)
    # print('P1: ', P1)
    # print('P2: ', P2)

    return L, G, P1, P2


def objective(alpha, beta, gamma, miu, A1, A2, G, P1, P2, M, Y1, Y2, E1, E2, Lambda1, Lambda2):
    O1 = numpy.sum(numpy.sqrt(numpy.sum(numpy.power(Y1 * (A1 - numpy.dot(G, P1)), 2), axis=1)), axis=0)
    O2 = numpy.sum(numpy.sqrt(numpy.sum(numpy.power(Y2 * (A2 - numpy.dot(G, P2)), 2), axis=1)), axis=0)
    D1 = numpy.diag(numpy.sum(M, axis=1))
    D2 = numpy.diag(numpy.sum(M, axis=0))
    O3 = (numpy.trace(P1.dot(D1).dot(P1.transpose())) + numpy.trace(P2.dot(D2).dot(P2.transpose())) - 2 * numpy.trace(
        P1.dot(M).dot(P2.transpose())))
    O4 = numpy.linalg.norm(G, ord='fro') ** 2 + numpy.linalg.norm(P1, ord='fro') ** 2 + numpy.linalg.norm(P2,
                                                                                                          ord='fro') ** 2
    # print(O1, O2, O3, O4)
    # print(alpha, beta, gamma)
    O = O1 + alpha * O2 + beta * O3 + gamma * O4

    O5 = numpy.sum(numpy.sqrt(numpy.sum(numpy.power(E1, 2), axis=1)), axis=0)
    O6 = numpy.sum(numpy.sqrt(numpy.sum(numpy.power(E2, 2), axis=1)), axis=0)
    O7 = numpy.linalg.norm(Y1 * (A1 - numpy.dot(G, P1)) - E1 + (1 / miu) * Lambda1, ord='fro') ** 2
    O8 = numpy.linalg.norm(Y2 * (A2 - numpy.dot(G, P2)) - E2 + (1 / miu) * Lambda2, ord='fro') ** 2
    OO = O5 + alpha * O6 + beta * O3 + gamma * O4 + (miu / 2) * (O7 + O8)

    # print('O: ', O)
    # print('OO: ', OO)
    return O, OO
