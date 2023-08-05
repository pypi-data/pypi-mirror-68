# coding:utf-8



'''
计算 模型分 最值，并自动划分区间，为最后展示分数做准备
'''


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lapras.Settings import col_head,woe_file_output
from lapras.DealConfig import params, A, B, theta, woe_all, cut_points_step, assist_num, bond_list, eps, get_GBK_Name
from lapras.DealConfig import makeModelDataFillnaFileName, scoreCardDataFileName, comParamCorrFileName, checkDataFileName,\
    scoreCardParamFileName, scoreCardPklFileName,woeFileName

import pickle
import math

def get_model_result():
    pass

# 将评分卡分数转换为概率
def score_to_prob(base_score, A=A, B=B):
    odds = math.pow(math.e,(A-base_score)/B)
    prob = odds/(1+odds)
    return prob

def get_score_max_min(A, B, theta, woe_all):
    # 计算当前 A, B, theta, woe_all 下 得分区间 （最大最小值）
    base_score_pri = A - B * theta[0]
    print ('base_score %s'%base_score_pri )
    base_score_max = base_score_pri
    base_score_min = base_score_pri
    for index_theta, theta_one in enumerate(theta):
        if index_theta == 0:
            continue
        base_score_min -= B * theta_one * max(woe_all[index_theta-1])
        base_score_max -= B * theta_one * min(woe_all[index_theta-1])
        a = 1
    print ('base_score_max %s'%base_score_max)
    print ('base_score_min %s' %base_score_min)
    return base_score_min, base_score_max

def get_score_csv(makeModelDataFillnaFileName='make_model_data_fillna_file.csv', scoreCardDataFileName='score_card_data_file.csv', comParamCorrFileName='com_param_corr_file.csv', checkDataFileName='check_data_storeout_file.csv', save_file=True):
    '''
    保存入模变量 变量相似性 得分结果
    :param makeModelDataFillnaFileName:  原始数据文件
    :param scoreCardDataFileName: 入模变量得分
    :param comParamCorrFileName: 入模变量相似度
    :param checkDataFileName: 每个样本得分
    :param save_file: 是否保存文件
    :return:
    '''
    # 读取 原始数据文件 获得入模变量数据
    try:
        df_data = pd.read_csv(makeModelDataFillnaFileName, encoding='utf-8')
    except:
        df_data = pd.read_csv(makeModelDataFillnaFileName, encoding='gbk')
    params_list = col_head + params
    df_params = df_data[params_list]

    woe_list = []

    # 整理 bond
    bond_all = list()
    for bond in bond_list:
        bond_all.append(['-inf'] + bond + ['inf'])
    data = df_params.drop([col_head[1]],axis=1).values.tolist()
    datay = df_params[col_head[1]].values.tolist()
    dim = len(bond_all)
    fo_list = list()
    for i in range(len(data)):
        cus_no = data[i][0]
        woe_list_tmp = [cus_no,df_params.iloc[i, 1]]

        base_score = A - B * theta[0]
        # print(base_score)
        for j in range(dim):
            cell = data[i][j + 1]
            bond = bond_all[j]
            woe = woe_all[j]
            woe_size = len(woe)
            index = -1
            for k in range(woe_size):
                # print(str(cus_no) + " " + str(bond))
                if k == 0 and cell < bond[k + 1]:
                    index = k
                if k > 0 and k < woe_size - 1 and cell > bond[k] - eps and cell < bond[k + 1]:
                    index = k
                if k == woe_size - 1 and cell > bond[k] - eps:
                    index = k
            # print (B * theta[j + 1] * woe[index])
            base_score -= (B * theta[j + 1] * woe[index])
            woe_list_tmp.append(woe[index])
        # print(base_score)
        fo_list.append([cus_no, datay[i], base_score, score_to_prob(base_score)])
        woe_list_tmp.append(base_score)
        woe_list.append(woe_list_tmp)



    #生成评分卡参数文件
    score_card_map = {}
    column = ['variable', 'bin', 'points']
    intercept = round(A - B * theta[0],2)
    df = pd.DataFrame(['basepoints' ,np.NAN, intercept]).T
    df.columns = column
    score_card_map['basepoints'] = df
    for j in range(len(bond_all)):
        bond = bond_all[j]
        woe = woe_all[j]
        woe_size = len(woe)
        index = -1
        df1 = pd.DataFrame(columns=column)
        for k in range(woe_size):
            if k == 0:
                bin_str = "[" + str(bond[k]) + "," + str(bond[k+1]) + ")"
            else:
                bin_str = "[" + str(bond[k]) + "," + str(bond[k + 1]) + ")"
            score = round(-(B * theta[j + 1] * woe[k]),2)
            df2 = pd.DataFrame([params[j],bin_str,score]).T
            df2.columns = column
            df1 = pd.concat([df1,df2],ignore_index=True)
        score_card_map[params[j]] = df1

    # 将数据序列化后存储到文件中
    f = open(scoreCardPklFileName, 'wb')  # pickle只能以二进制格式存储数据到文件
    f.write(pickle.dumps(score_card_map))  # dumps序列化源数据后写入文件
    f.close()
    f = open(scoreCardParamFileName, 'w')  # 写入文本文件
    f.write(str(score_card_map))
    f.close()


    print ('save_file')
    if save_file:
        # 保存入模变量
        try:
            df_params.to_csv(scoreCardDataFileName, index=None, encoding='utf-8')
            # df_params.to_csv(get_GBK_Name(scoreCardDataFileName), index=None, encoding='gbk')
            print ('save scoreCardDataFileName success')
        except:
            print('error in save scoreCardDataFileName')
        # 保存 变量相似性
        df_data[params].corr().to_csv( comParamCorrFileName, index=None, encoding='utf-8', )
        print('save comParamCorrFileName success')
        if woe_file_output:
            pd.DataFrame(woe_list, columns=params_list + ['base_score']).to_csv( woeFileName, index=None, encoding='utf-8')
            print('save woe file success')

        # 保存得分结果
        # df_fo = pd.DataFrame(fo_list, columns=['cus_no', 'y', 'base_score'])
        df_fo = pd.DataFrame(fo_list, columns=col_head + ['base_score','default_prob'])
        try:
            df_fo.to_csv(checkDataFileName, index=False, encoding='utf-8')
            # df_fo.to_csv(get_GBK_Name(checkDataFileName), index=False, encoding='gbk')
            print ('save checkDataFileName success')
        except:
            print('error in save checkDataFileName')
    return

def get_score_bond(cut_points_step, assist_num=assist_num, minpoint=200, maxpoint=1000,  checkDataFileName='check_data_file.csv'):
    try:
        scoredata = pd.read_csv(checkDataFileName, encoding='utf-8')
    except:
        scoredata = pd.read_csv(checkDataFileName, encoding='gbk')

    base_score = scoredata['base_score']
    base_score_max = max(base_score)
    base_score_min = min(base_score)
    maxpoint = int(maxpoint) + 1
    minpoint = int(minpoint) - 1
    cutmin = int(base_score_min / 10.0) * 10
    cutmax = int((base_score_max / 10.0) * 10)
    while (scoredata[(scoredata['base_score'] <= cutmin) & (scoredata[col_head[1]] == 0)]['base_score'].count() < 20 or scoredata[(scoredata['base_score'] <= cutmin) & (scoredata[col_head[1]] == 1)]['base_score'].count() < 1):
        cutmin = cutmin + 10
    while (scoredata[(scoredata['base_score'] >= cutmax) & (scoredata[col_head[1]] == 0)]['base_score'].count() < 20 or scoredata[(scoredata['base_score'] >= cutmax) & (scoredata[col_head[1]] == 1)]['base_score'].count() < 1):
        cutmax = cutmax - 10
    cut_points = list(range(cutmin, cutmax + assist_num * cut_points_step, cut_points_step))
    break_points = [minpoint] + cut_points + [maxpoint]
    return break_points


