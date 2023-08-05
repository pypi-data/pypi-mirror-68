# coding:utf-8

import numpy as np


def sigmoidFunction(X, theta):
    return 1.0 / (1.0 + np.exp(-X.dot(theta)))


def f_logistic(theta, X, y, lamb):
    (m, n) = X.shape
    # print theta
    h = sigmoidFunction(X, theta.reshape(n, 1)).reshape(m, )
    # print h
    J = -(1.0 / m) * (np.inner(y, np.log(h)) + np.inner((1.0 - y), np.log(1.0 - h))) + (lamb / 2.0 / m) * np.sum(
        np.square(theta[1:]))
    # print J
    return J


def fgrad_logistic(theta, X, y, lamb):
    (m, n) = X.shape
    h = sigmoidFunction(X, theta.reshape(n, 1)).reshape(m, )
    temp = lamb * theta
    temp[0] = 0.0
    grad = (1. / m) * (X.T.dot((h - y).reshape(m, 1)) + temp.reshape(n, 1))
    return grad.reshape(n, )


def f_linear(theta, X, y, lamb):
    (m, n) = X.shape
    J = (0.5 / m) * np.sum(np.square(y - X.dot(theta.reshape(n, 1))))
    return J


def fgrad_linear(theta, X, y, lamb):
    (m, n) = X.shape
    grad = (1.0 / m) * ((X.dot(theta.reshape(n, 1)) - y) * X)
    return np.sum(grad, 0)

