# coding:utf-8

import numpy as np
import scipy.optimize as opt
from lapras.code.utils import cost


def startTrain(trainx, trainy, lamb, type='logistic'):
    m = trainx.shape[0]
    n = trainx.shape[1] + 1
    # print m,n
    X = np.column_stack((np.ones((m, 1), dtype=float), trainx))
    # print X
    y = trainy
    min_J = np.inf
    min_theta = np.zeros(n)
    eps = 0.1
    if type == 'logistic':
        f = cost.f_logistic
        fgrad = cost.fgrad_logistic
    elif type == 'linear':
        f = cost.f_linear
        fgrad = cost.fgrad_linear
    for i in range(30):
        init_theta = np.random.rand(n) * 2.0 * eps - eps
        # print init_theta
        theta = opt.fmin_cg(f, init_theta, fprime=fgrad, args=(X, y, lamb), disp=False)
        # print theta
        J = f(theta, X, y, lamb)
        if J < min_J:
            min_J = J
            min_theta = theta
    return min_theta

