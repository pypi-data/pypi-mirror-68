# coding:utf-8

import numpy as np
import matplotlib.pyplot as plot
import pandas as pd

from sklearn.metrics import roc_curve

from lapras.code.utils import cost
from lapras.code.utils import train


from lapras.code.utils.FileUtil import write_data
from lapras.DealConfig import OutModelFileName


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


def KS(testx, testy, theta, ks_bucket_num=10):
    tot_bad = np.sum(testy == 1)
    tot_good = np.sum(testy == 0)
    testx = np.column_stack((np.ones((testx.shape[0], 1), dtype=float), testx))
    n = theta.shape[0]
    h = cost.sigmoidFunction(testx, theta.reshape(n, 1)) # prob
    data = np.column_stack((h, testy))
    data = data[np.argsort(data[:, 0])]
    # np.random.shuffle(data)
    m = data.shape[0]
    sum_bad_percent = [0.0]
    sum_good_percent = [0.0]
    score = []
    for i in range(ks_bucket_num):
        if i == ks_bucket_num - 1:
            data_seg = data[int(m * i / ks_bucket_num):]
        else:
            data_seg = data[int(m * i / ks_bucket_num):int(m * (i + 1) / ks_bucket_num)]
        bad = np.sum(data_seg[:, 1] == 1)
        good = np.sum(data_seg[:, 1] == 0)
        if good == 0:
            percent = 999.0
        else:
            percent = 1.0 * bad / good
        score.append([percent, bad, good])
    score = np.array(score)
    score = score[np.argsort(score[:, 0])]
    # print score
    for i in range(ks_bucket_num):
        # i = 10 - j - 1
        bad = score[i, 1]
        good = score[i, 2]
        # print bad, good, score[i, 0]
        bad_percent = 1.0 * bad / tot_bad
        good_percent = 1.0 * good / tot_good
        sum_bad_percent.append(sum_bad_percent[-1] + bad_percent)
        sum_good_percent.append(sum_good_percent[-1] + good_percent)
    sum_bad_percent = np.array(sum_bad_percent)
    sum_good_percent = np.array(sum_good_percent)
    ks = np.max(sum_good_percent - sum_bad_percent)
    # print 'k-s = %f ' % (ks)
    return (ks, sum_bad_percent, sum_good_percent)


def ROC(testx, testy, theta):
    m = testx.shape[0]
    n = testx.shape[1] + 1
    testx = np.column_stack((np.ones((m, 1), dtype=float), testx))
    n = theta.shape[0]
    h = cost.sigmoidFunction(testx, theta.reshape(n, 1)).reshape(m, )
    TPR_num = []
    FNR_num = []
    tot_true = np.sum(testy == 1)
    tot_false = np.sum(testy == 0)
    alpha_list = np.linspace(0, 1, 1001)
    for alpha in alpha_list:
        TPR_num.append(np.sum(np.bitwise_and(testy == 1, h >= alpha)))
        FNR_num.append(np.sum(np.bitwise_and(testy == 0, h < alpha)))
    TPR_num = np.array(TPR_num)
    FNR_num = np.array(FNR_num)
    TPR = 1.0 * TPR_num / tot_true
    FNR = 1.0 - 1.0 * FNR_num / tot_false
    length = len(TPR)
    AUC = 0.0
    for i in range(length - 1):
        AUC += (TPR[i] + TPR[i + 1]) * (FNR[i] - FNR[i + 1]) / 2.0
    # print 'AUC = %f ' % AUC
    return (AUC, FNR, TPR)



def WOE(dim_name, data, dim, bucket_num=10, auto=True, bond_num=[]):
    # (trainx, trainy, testx, testy) = ld.getTrainTest(data)
    m = data.shape[0]
    X = data[:, dim]
    y = data[:, -1]
    tot_bad = np.sum(y == 1)
    tot_good = np.sum(y == 0)
    data = np.column_stack((X.reshape(m, 1), y.reshape(m, 1)))
    cnt_bad = []
    cnt_good = []
    min = np.min(data[:, 0])
    max = np.max(data[:, 0])
    if auto == True:

        index = np.linspace(min, max, bucket_num + 1)
    else:
        index = bond_num
        bucket_num = bond_num.shape[0] - 1
    data_bad = data[data[:, 1] == 1, 0]
    data_good = data[data[:, 1] == 0, 0]
    eps = 1e-8
    for i in range(bucket_num):
        if i < bucket_num - 1:
            cnt_bad.append(1.0 * np.sum(np.bitwise_and(data_bad > index[i] - eps, data_bad < index[i + 1])))
            cnt_good.append(1.0 * np.sum(np.bitwise_and(data_good > index[i] - eps, data_good < index[i + 1])))
        else:
            cnt_bad.append(1.0 * np.sum(np.bitwise_and(data_bad > index[i] - eps, data_bad < index[i + 1] + eps)))
            cnt_good.append(1.0 * np.sum(np.bitwise_and(data_good > index[i] - eps, data_good < index[i + 1] + eps)))
    bond = np.array(index)
    cnt_bad = np.array(cnt_bad)
    cnt_good = np.array(cnt_good)

    # cnt_bad[cnt_bad==0] += 1
    # cnt_good[cnt_good==0] += 1


    length = cnt_bad.shape[0]
    for i in range(length):
        j = length - i - 1
        if j != 0:
            if cnt_bad[j] == 0 or cnt_good[j] == 0:
                cnt_bad[j - 1] += cnt_bad[j]
                cnt_good[j - 1] += cnt_good[j]
                cnt_bad = np.append(cnt_bad[:j], cnt_bad[j + 1:])
                cnt_good = np.append(cnt_good[:j], cnt_good[j + 1:])
                bond = np.append(bond[:j], bond[j + 1:])
    if cnt_bad[0] == 0 or cnt_good[0] == 0:
        cnt_bad[1] += cnt_bad[0]
        cnt_good[1] += cnt_good[0]
        cnt_bad = cnt_bad[1:]
        cnt_good = cnt_good[1:]
        bond = np.append(bond[0], bond[2:])
    woe = np.log((cnt_bad / tot_bad) / (cnt_good / tot_good))
    IV = ((cnt_bad / tot_bad) - (cnt_good / tot_good)) * woe
    IV_tot = np.sum(IV)
    bond_str = []
    for b in bond:
        bond_str.append(str(b))
    # print 'IV = %f ' % IV_tot

    cnt_bad_list = cnt_bad.tolist()
    cnt_good_list = cnt_good.tolist()
    cnt_rate = list()
    for index_cnt, cnt in enumerate(cnt_bad):
        cnt_rate.append(float('%.04f'%(cnt/(cnt+cnt_good_list[index_cnt]))))

    out_1 = 'python_out "%s":%s' % (dim_name.strip(), bond_str)
    out_2 = '"cnt_good":%s,"cnt_bad":%s,"cnt_bad_rate":%s' % (cnt_good.tolist(), cnt_bad.tolist(), cnt_rate)
    out_3 = '"woe":%s,"IV":%s' % (woe.tolist(), IV_tot.tolist())
    print (out_1 + ', '+  out_2 +', '+  out_3)

    write_1 = 'python_out "%s":%s' % (dim_name.strip(), bond_str)
    write_2 = '"cnt_good":%s\t"cnt_bad":%s\t"cnt_bad_rate":%s' % (cnt_good.tolist(), cnt_bad.tolist(), cnt_rate)
    write_3 = '"woe":%s\t"IV":%s' % (woe.tolist(), IV_tot.tolist())
    write_data(OutModelFileName, write_1 + '\t'+  write_2 +'\t'+  write_3)

    return IV_tot, IV, woe, bond, cnt_rate, cnt_good, cnt_bad


def PSI(trainx, testx, trainy, testy, theta):

    testx = np.column_stack((np.ones((testx.shape[0], 1), dtype=float), testx))
    n = theta.shape[0]
    testp = cost.sigmoidFunction(testx, theta.reshape(n, 1)) # prob

    trainx = np.column_stack((np.ones((trainx.shape[0], 1), dtype=float), trainx))
    n = theta.shape[0]
    trainp = cost.sigmoidFunction(trainx, theta.reshape(n, 1)) # prob

    probability_train_list = list()
    cus_num_train_list = list()
    for index_tp, tp in enumerate(trainp):
        probability_train_list.append(tp[0])
        cus_num_train_list.append(index_tp)

    data_left = pd.DataFrame({'probability':probability_train_list, 'cus_num':cus_num_train_list, 'y':trainy},
                              columns=['probability', 'cus_num', 'y'])

    probability_test_list = list()
    cus_num_test_list = list()
    for index_tp, tp in enumerate(testp):
        probability_test_list.append(tp[0])
        cus_num_test_list.append(index_tp)

    data_right = pd.DataFrame({'probability':probability_test_list, 'cus_num':cus_num_test_list, 'y':testy},
                              columns=['probability', 'cus_num', 'y'])

    non_computed = None
    plot_image = True
    check_cols = ['probability', 'y', 'cus_num']
    if non_computed != None and type(non_computed) == str:
        check_cols += [non_computed]
        data_left = data_left[~data_left[non_computed] == True].copy()
        data_right = data_right[~data_right[non_computed] == True].copy()
    elif non_computed == None:
        data_left = data_left.copy()
        data_right = data_right.copy()
    else:
        raise ValueError('non_computed must be a str.')
    for col in check_cols:
        if col not in data_left.columns or col not in data_right.columns:
            raise ValueError('There is no column %s of data' % col)

    """Drop NaN and sort values by column 'probability'."""
    data_left = data_left.loc[data_left['probability'].notnull(), check_cols]
    data_right = data_right.loc[data_right['probability'].notnull(), check_cols]
    data_left.sort_values(by=['probability'], inplace=True, ascending=False)
    data_right.sort_values(by=['probability'], inplace=True, ascending=False)
    data_left.reset_index(drop=True, inplace=True)
    data_right.reset_index(drop=True, inplace=True)

    """Discrete probability value."""
    break_points_left = [int(data_left.shape[0] * i) for i in np.arange(0.0, 1.1, 0.1)]
    break_points_right = [int(data_right.shape[0] * i) for i in np.arange(0.0, 1.1, 0.1)]
    quantile_str = [str(i) + '%' for i in np.arange(10, 110, 10)]
    for i in range(len(break_points_left)):
        if i == len(break_points_left) - 1:
            break
        else:
            data_left.loc[break_points_left[i]:break_points_left[i + 1], 'quantile'] = quantile_str[i]
            data_right.loc[break_points_right[i]:break_points_right[i + 1], 'quantile'] = quantile_str[i]

    """Count psi of bad & good sample."""
    count_left = data_left.groupby(['quantile', 'y']).count()['cus_num'].unstack().fillna(value=0.0)
    count_right = data_right.groupby(['quantile', 'y']).count()['cus_num'].unstack().fillna(value=0.0)


    a = 0

    try:
        if count_left[1].sum() == 0 or count_right[1].sum() == 0:
            a = 1
            return 0, 1
        if count_left[0].sum() == 0 or count_right[0].sum() == 0:
            a = 1
            return 0, 1

    except:
        a = 1
        return 0, 1

    count_left['bad_ratio'] = count_left[1] / count_left[1].sum()
    count_right['bad_ratio'] = count_right[1] / count_right[1].sum()
    count_left['good_ratio'] = count_left[0] / count_left[0].sum()
    count_right['good_ratio'] = count_right[0] / count_right[0].sum()
    count_final = pd.merge(count_left, count_right, left_index=True,
                           right_index=True, suffixes=['_left', '_right'])
    count_final['psi_bad'] = (count_left['bad_ratio'] - count_right['bad_ratio']) * np.log(count_left['bad_ratio'] / count_right['bad_ratio'])
    count_final['psi_good'] = (count_left['good_ratio'] - count_right['good_ratio']) * np.log(count_left['good_ratio'] / count_right['good_ratio'])
    count_final = count_final.reindex(quantile_str)
    average_psi = (count_final['psi_bad'].replace([np.inf, np.nan], 0.0).sum() + count_final['psi_good'].replace([np.inf, np.nan], 0.0).sum()) / 2

    print ('Average PSI:%f' % average_psi )
    write_data(OutModelFileName, 'Average PSI:%f' % average_psi)


    if 0 in list(count_right['bad_ratio'].values) or 0 in list(count_right['good_ratio']):
        a = 1


    return average_psi, a


def calcVIF(data, columns_dim):
    m = data.shape[0]
    n = data.shape[1] - 1

    VIF_list = list()

    if n < 2:
        print ('python_out \"VIF\":-1')
        VIF_list.append(-1)
        return
    for i in range(n):
        newy = data[:, i].reshape(m, 1)
        newX = np.column_stack((data[:, :i], data[:, i + 1:n]))
        # print data[:, 0]

        theta = train.startTrain(newX, newy, 0, type='linear').reshape(n, 1)
        # print theta
        newX = np.column_stack((np.ones((m, 1), dtype=float), newX))
        predict = newX.dot(theta).reshape(m, )
        newy = newy.reshape(m, )
        # VIF.append(np.sum(np.square(newy-np.mean(newy)))/np.sum(np.square(predict-newy)))
        VIF = np.sum(np.square(newy - np.mean(newy))) / np.sum(np.square(predict - newy))

        VIF_list.append(':%f' % VIF)

        print ('python_out \"VIF\":%f' % VIF + " " + str(columns_dim[i]))
        # return VIF
    # print('python_out' + str(VIF_list))

    write_data(OutModelFileName, 'python_out' + str(VIF_list))

    return


if __name__ == '__main__':
    pass
