import os
import random as rand
import sys
import numpy as np
import pandas as pd
from lapras.DealConfig import makeModelDataFillnaFileName, OnlyModelDataFillnaFileName
from lapras.code.DealParamConfig import params
from lapras.Settings import col_head


def get_only_model_data():
    param_list = col_head + params
    df_data = pd.read_csv(makeModelDataFillnaFileName)
    df_data = df_data.dropna(how='all')
    df_data[param_list].to_csv(OnlyModelDataFillnaFileName, index=None, encoding='utf-8')




def rankData(data, dim, bond, woe):
    data_dim = data[:, dim]
    m = data_dim.shape[0]
    b = bond.shape[0]
    eps = 1e-8
    for i in range(m):
        xi = float(data_dim[i])
        bond_index = -1
        for j in range(b - 1):
            if (j < b - 2 and xi > bond[j] - eps and xi < bond[j + 1]) or (
                                j == b - 2 and xi > bond[j] - eps and xi < bond[j + 1] + eps):
                bond_index = j
        data_dim[i] = woe[bond_index]
    return data


def getTrainTest(data, sep=-1):
    if sep == -1:
        np.random.shuffle(data)
        sep = int(data.shape[0] * 0.7)
    trainx = data[:sep, :-1]
    trainy = data[:sep, -1]
    testx = data[sep:, :-1]
    testy = data[sep:, -1]
    return 1. * trainx, 1. * trainy, 1. * testx, 1. * testy

