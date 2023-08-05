# coding:utf-8

import math
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve

from lapras.DealConfig import checkDataFileName
from lapras.Settings import col_head




def ks_calc_cross(pred, y_label):
    '''
    功能: 计算KS值，输出对应分割点和累计分布函数曲线图
    输入值:
    data: 二维数组或dataframe，包括模型得分和真实的标签
    pred: 一维数组或series，代表模型得分（一般为预测正类的概率）
    y_label: 一维数组或series，代表真实的标签（{0,1}或{-1,1}）
    输出值:
    'ks': KS值，'crossdens': 好坏客户累积概率分布以及其差值gap
    '''
    crossfreq = pd.crosstab(pred, y_label)
    crossdens = crossfreq.cumsum(axis=0) / crossfreq.sum()
    crossdens['gap'] = abs(crossdens[0] - crossdens[1])
    ks = crossdens[crossdens['gap'] == crossdens['gap'].max()]
    return float(ks['gap'])


def ks_calc_auc(pred, y_label):
    '''
    功能: 计算KS值，输出对应分割点和累计分布函数曲线图
    输入值:
    data: 二维数组或dataframe，包括模型得分和真实的标签
    pred: 一维数组或series，代表模型得分（一般为预测正类的概率）
    y_label: 一维数组或series，代表真实的标签（{0,1}或{-1,1}）
    输出值:
    'ks': KS值
    '''
    fpr, tpr, thresholds = roc_curve(y_label, pred)
    ks = max(tpr - fpr)
    return ks


'''
运行代码主文件

使用时请注释掉不需要运行的行
'''

def performance(checkDataFileName=checkDataFileName,bad_label=col_head[1]):

    df = pd.read_csv(checkDataFileName, engine='python', encoding='utf-8')
    df["rank"] = 1000 - df['base_score']

    # AUC值 KS值
    precisions, recalls, thresholds = precision_recall_curve(df[bad_label], df["rank"])
    fpr, tpr, thresholds = roc_curve(df[bad_label], df["rank"])
    auc = roc_auc_score(df[bad_label], df["rank"])
    ks = max(tpr - fpr)
    print("KS: %.4f" % (ks))
    print("AUC: %.4f"  % (auc))

    # 设置图形大小
    plt.rcParams['figure.figsize'] = (12.0, 8.0)
    plt.rcParams.update({'font.size': 20})

    # 绘制AUC曲线
    # plt.legend(('train_set', 'test_set', 'OOT1', 'OOT2', 'OOT3'), loc='lower right')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Line')
    plt.plot(fpr[:-1], tpr[:-1])
    plt.show()

    # 绘制KS曲线
    x_axis = [i / len(tpr[:-1]) for i in range(len(tpr[:-1]))]
    position = np.argmax(tpr - fpr)
    plot_position = position / len(tpr[:-1])
    plt.plot(x_axis, tpr[:-1])
    plt.plot(x_axis, fpr[:-1])
    plt.plot([plot_position, plot_position], [tpr[position], fpr[position]])
    plt.legend(('True Positive', 'False Positive', 'Max Ks Gap'), loc='upper left')
    plt.xlabel('Percent')
    plt.ylabel('Rate')
    plt.text(0.5, 0.5, 'ks=' + str(round(ks, 3)))
    plt.title('KS Line')
    plt.show()

    # 绘制PR曲线
    plt.plot(recalls[:-1], precisions[:-1])
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('PR Line')
    plt.show()

    # 计算PR
    tmp = pd.DataFrame([recalls[:-1], precisions[:-1]]).T
    tmp.columns = ['recalls', 'precisions']
    recalls = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    for recall in recalls:
        presion = 0.002
        d = tmp[(tmp['recalls'] >= recall - presion) & (tmp['recalls'] <= recall + presion)].reset_index(drop=True)
        print(d.iloc[:1, :])