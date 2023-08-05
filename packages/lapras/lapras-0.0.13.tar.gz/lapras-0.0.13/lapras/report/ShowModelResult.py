# coding:utf-8


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



from lapras.DealConfig import checkDataFileName, makeModelDataFillnaFileName, scoreCardDataFileName, comParamCorrFileName
from lapras.DealConfig import A, B, theta, woe_all, cut_points_step, assist_num
from lapras.ReportConfig import  cut_points_step, assist_num, score_bond

from lapras.report.ScoreParam import get_score_csv, get_score_max_min, get_score_bond
from lapras.report.MakeModelDoc import count_point, plt_show



'''
模型效果展示  

整合数据 得到对应图表， 并打印部分统计数据
'''

def show_pic(score_bond):
    # 保存入模变量 变量相似性 得分结果

    # 计算 区间数量 区间坏账率
    x, ticks, y_count, y_rate = count_point(checkDataFileName, score_bond)

    # 画图显示 区间数量 区间坏账率
    plt_show(x, ticks, y_count, y_rate)

def show_model_pic(score_bond):


    get_score_csv(makeModelDataFillnaFileName, scoreCardDataFileName, comParamCorrFileName, checkDataFileName)
    if not score_bond:
        # 得到计分区间
        base_score_min, base_score_max = get_score_max_min(A, B, theta, woe_all)
        # 自动划分区间
        score_bond = get_score_bond(cut_points_step, assist_num=assist_num, minpoint=base_score_min, maxpoint=base_score_max, checkDataFileName=checkDataFileName)

    print(score_bond)

    # 展示效果
    show_pic(score_bond)
    # 为写模型部署文档准备表格数据
    # make_model_doc(params, theta, woe_all, param_bond, B)

