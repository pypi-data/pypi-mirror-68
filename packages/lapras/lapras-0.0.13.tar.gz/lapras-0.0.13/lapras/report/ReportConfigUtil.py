# coding:utf-8

import re

'''
切割 模型代码 print 的 结果， 专门用于手动复制的情况 处理得到 画图参数
'''

def get_param_bond_woe_all_theta(str_data):

    params_theta = str_data.split('to_csv_success')
    params = params_theta[0]
    thetas = params_theta[1]

    param_bond = dict()
    woe_all = list()

    params_re_findall = re.findall('python_out.*?\n', params)
    for params_re in params_re_findall:
        param_name = re.findall('"(.*?)"', params_re)[0]
        bond = eval(re.findall('\[.*?\]', params_re)[0])
        # cnt_good = re.findall('\[.*?\]', params_re)[1]
        # cnt_bad = re.findall('\[.*?\]', params_re)[2]
        # bad_rate = re.findall('\[.*?\]', params_re)[3]
        woe = re.findall('\[.*?\]', params_re)[4]
        woe_all.append(eval(woe))

        param_bond[param_name] = [eval(bd) for bd in bond if 'inf' not in bd]
    theta = eval(re.findall('"theta":(.*?)\n', thetas)[0])
    params = list(param_bond.keys())
    bond_list = [param_bond.get(para) for para in params]
    return params, param_bond, woe_all, theta, bond_list

def get_GBK_Name(filename):
    if isinstance(filename, str):
        if filename.count('.') == 1:
            if '.' in filename:
                return filename.split('.')[0] + 'GBK.' + filename.split('.')[1]
    return filename

