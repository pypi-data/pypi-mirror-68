# coding:utf-8

import numpy as np
import pandas as pd
from copy import deepcopy

from lapras.code.utils import decisionTree as dt
from lapras.code.utils import perform as perf
from lapras.code.utils import train
from lapras.code import loadData as ld
from lapras.code.DealParamConfig import bin_params, minLeaf, treeDepth, bucketnum
from lapras.code.utils.FileUtil import write_data, deal_data
from lapras.DealConfig import OutModelFileName


def load_data(path):
    companylist = list()
    with open(path) as f:
        data=[]
        columns = list()
        for index_l, line in enumerate(f):
            if index_l==0:
                columns = line
                continue

            cols=line.strip().split(',')
            companylist.append(cols[0])
            line_data=[float(x) for x in cols[2:]]


            line_data.append(float(cols[1]))

            data.append(line_data)
    f.close()
    return np.array(data), columns.split(','), companylist



def state_data(new_file_name, rule_file_name=None, makemodel=1):
    print ('读取 new_file_name')

    deal_data(OutModelFileName)

    data, columns, companylist = load_data(new_file_name)

    dims = len(columns) -2
    test_case = 1
    init_flag_list = [1]*dims # 特征数 list
    # 分箱方法
    eql_dis_flag_list = [0]*dims # 等段分箱

    if makemodel == 1:
        tree_flag_list = [0] * dims  # 决策树分箱 1采用 0 不采用
        bond_list = deepcopy(bin_params)

    else:
        tree_flag_list = [1] * dims  # 决策树分箱 1采用 0 不采用
        bond_list = [0] * dims

    # 离散桶
    bucketnum_list = [bucketnum]*dims
    # 树深度
    treeDepth_list = [treeDepth]*dims
    # 最小子数目
    # minLeaf_list = [1]*dims
    minLeaf_list = [minLeaf]*dims

    X_dim = len(init_flag_list)

    res_arr = None

    columns_dim = columns[2:]
    woe_list = []
    print('计算 WOE')
    for i in range(X_dim):
        if tree_flag_list[i] == 1:
            bond_list[i] = dt.decisionTreeSplit(data[:, i], data[:, -1], treeDepth_list[i], minLeaf_list[i])
        bond_list[i].insert(0, -np.inf)
        bond_list[i].append(np.inf)
        bond_list[i] = np.sort(np.array(bond_list[i]))
        IV_tot, IV, woe, bond, cnt_rate, cnt_good, cnt_bad = perf.WOE(columns_dim[i], data, i,
                                                                      bucket_num=bucketnum_list[i],
                                                                      auto=(eql_dis_flag_list[i] == 1),
                                                                      bond_num=bond_list[i])
        bond_list[i] = bond
        woe_list.append(woe)

        trend_list = list(cnt_rate)
        trend = ''
        if len(trend_list) > 1:
            for index_cnt_rate, cnt_rate_i in enumerate(trend_list[1:]):
                if cnt_rate_i > trend_list[index_cnt_rate]:
                    trend = trend + '+'
                elif cnt_rate_i < trend_list[index_cnt_rate]:
                    trend = trend + '-'
                else:
                    trend = trend + '='
        else:
            trend = '/'

        dim_arr = np.array([columns_dim[i].strip(), str(list(bond)), str(list(cnt_good)), str(list(cnt_bad)), str(list(cnt_rate)), trend, str(list(woe)), str(list(IV)), float('%.08f' % IV_tot), float('%.03f' % IV_tot)])
        if res_arr is None:
            res_arr = dim_arr
        else:
            res_arr = np.vstack((res_arr, dim_arr))

    columns = ['dim_name', 'bin', 'cnt_good', 'cnt_bad', 'cnt_bad_rate', 'trend','woe', 'IV_i', 'IV', 'IV_sort']
    df = pd.DataFrame(res_arr, columns=columns)
    # df = df.sort_values(by=['IV'], ascending=False)
    df = df.sort_values(by=['IV_sort'], ascending=False)

    # df.to_csv('rule_valid.csv', index=False, header=columns)
    columns.pop()
    df.drop(['IV_sort'], axis=1).to_csv(rule_file_name, index=False, header=columns)
    print('to_csv_success')
    write_data(OutModelFileName, 'to_csv_success')

    # 输出自动分箱结果
    bin_map = {}
    for index, row in df.iterrows():
        bin_map[row['dim_name']] = row['bin']
    print(bin_map)




    if makemodel == 1:
        ks = []
        ks_index = []
        ks_train = []
        ks_index_train = []

        ROC_index = []
        ROC = []
        theta_all = []

        ks_big = []
        ks_index_big = []
        ks_train_big = []
        ks_index_train_big = []

        ROC_index_big = []
        ROC_big = []
        theta_all_big = []

        # initialize data
        for i in range(X_dim):
            if init_flag_list[i] == 1:
                data = ld.rankData(data, i, bond_list[i], woe_list[i])
        # pd.DataFrame(data).to_csv("C:\\Users\\20160822\\Desktop\\Features.csv")

        sum_ks = 0.0
        sum_ks_train = 0.0
        sum_auc = 0.0
        sum_ks_big = 0.0
        sum_ks_train_big = 0.0
        sum_auc_big = 0.0
        is_good = 0
        ii = 0
        jj = 0
        for i in range(test_case):
            print('test case # %d' % (i + 1))
            (trainx, trainy, testx, testy) = ld.getTrainTest(data)
            theta = train.startTrain(trainx, trainy, 0.0)
            (ks_temp, dummy1, dummy2) = perf.KS(testx, testy, theta)
            (ks_temp_train, dummy1_train, dummy2_train) = perf.KS(trainx, trainy, theta)
            if ks_temp_train > ks_temp:
                is_good = 1
                theta_all.append(theta)
                sum_ks += 1.0 * ks_temp
                ks.append((ks_temp, dummy1, dummy2))
                ks_index.append(ks_temp)
                sum_ks_train += 1.0 * ks_temp_train
                ks_train.append((ks_temp_train, dummy1_train, dummy2_train))
                ROC.append(perf.ROC(testx, testy, theta))
                # ROC_index.append(ROC[-1][0])
                sum_auc += 1.0 * ROC[ii][0]
                ii += 1
            else:
                theta_all_big.append(theta)
                sum_ks_big += 1.0 * ks_temp
                ks_big.append((ks_temp, dummy1, dummy2))
                ks_index_big.append(ks_temp)
                sum_ks_train_big += 1.0 * ks_temp_train
                ks_train_big.append((ks_temp_train, dummy1_train, dummy2_train))
                ROC_big.append(perf.ROC(testx, testy, theta))
                # ROC_index_big.append(ROC[-1][0])
                sum_auc_big += 1.0 * ROC_big[jj][0]
                jj += 1

        if is_good == 0:
            theta_all = theta_all_big
            ks = ks_big
            ks_train = ks_train_big
            ROC = ROC_big
            ks_index = ks_index_big
            # ROC_index = ROC_index_big
        ks_index = np.array(ks_index)
        # ROC_index = np.array(ROC_index)
        ks_max_index = np.argmax(ks_index)
        # ROC_max_index = np.argmax(ROC_index)
        print('计算 calcVIF')
        perf.calcVIF(data, columns_dim)


        print_1 = '\"theta\":%s' % theta_all[ks_max_index].tolist()
        print_2 = '\"max_k-s\":%f' % ks[ks_max_index][0]
        print_3 = '\"max_k-s_train\":%f' % ks_train[ks_max_index][0]
        print_4 = '\"max_AUC\":%f' % ROC[ks_max_index][0]
        print_5 = '\"avg_k-s\":%f' % ((sum_ks + sum_ks_big) / test_case)
        print_6 = '\"avg_AUC\":%f' % ((sum_auc + sum_auc_big) / test_case)

        str_out_print = print_1 + '\n' + print_2 + '\n' + print_3 + '\n' + print_4 + '\n' + print_5 + '\n' + print_6
        print (str_out_print)
        # print('python_out \"theta\":%s' % theta_all[ks_max_index].tolist())
        # print (min(theta_all[ks_max_index].tolist()[1:]))
        # print
        # print('python_out \"max_k-s\":%f' % ks[ks_max_index][0])
        # print('python_out \"max_k-s_train\":%f' % ks_train[ks_max_index][0])
        # print('python_out \"max_AUC\":%f' % ROC[ks_max_index][0])

        # print
        # print('python_out \"avg_k-s\":%f' % ((sum_ks + sum_ks_big) / test_case))
        # print('python_out \"avg_AUC\":%f' % ((sum_auc + sum_auc_big) / test_case))
        average_psi, a = perf.PSI(trainx, testx, trainy, testy, theta)
        # perf.KS_draw(ks[ks_max_index][1], ks[ks_max_index][2])
        # perf.ROC_draw(ROC[ks_max_index][1], ROC[ks_max_index][2])

        write_data(OutModelFileName,  str_out_print)
        return perf, ks, ks_train,ROC, ks_max_index,average_psi, a, min(theta_all[ks_max_index].tolist()[1:])
    else:
        return None