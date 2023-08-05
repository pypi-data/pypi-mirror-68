# coding:utf-8

# 设置环境变量
import pandas as pd

from lapras.code import AnalyzeData

from lapras.DealConfig import makeModelDataFillnaFileName, ruleFilePriName
from lapras.DealConfig import OnlyModelDataFillnaFileName, ruleModelFilePriName, ruleModelFileName
from lapras.code.loadData import get_only_model_data

'''
    # 规则 建模模块
    # 0是所有变量的单次跑
    # 1是单次建模
    # 2是循环直到合适的数据
'''
def run_model( run_type_cus=-1):
    # 建模
    if run_type_cus == 0:
        AnalyzeData.state_data(makeModelDataFillnaFileName,ruleFilePriName, 0)
    elif run_type_cus == 1:
        get_only_model_data()
        AnalyzeData.state_data(OnlyModelDataFillnaFileName, ruleModelFileName, 1)
    elif run_type_cus == 2:
        get_only_model_data()
        while True:
            perf, ks, ks_train, ROC,ks_max_index, average_psi, a, min_theta = AnalyzeData.state_data(OnlyModelDataFillnaFileName, ruleModelFilePriName, 1)
            ks_max = ks[ks_max_index][0]
            ks_train_max = ks_train[ks_max_index][0]
            if ks_max < 0.25:
                continue
            if ks_max - ks_train_max > 0.03:
                continue
            if average_psi < 0.1 and min_theta > 0 and a == 0:
                perf.KS_draw(ks[ks_max_index][1], ks[ks_max_index][2])
                perf.ROC_draw(ROC[ks_max_index][1], ROC[ks_max_index][2])
                break




