# coding:utf-8

import re
# from DealConfig import csvFile
from lapras.report.MakeModelDoc import plt_show


def get_params_data_dict(model_name):
    with open(model_name, 'r') as f:
        params_data = f.read()
    f.close()

    params_data_valid_s = re.findall('(python_out.*?)\nAverage', params_data, re.S)
    if params_data_valid_s:
        params_data_valid = params_data_valid_s[-1]
    else:
        print ('model文件有误，请检查文件格式')
        return
    params_data_list = params_data_valid.split('\n')

    params_data_dict = dict()
    for params_data_one in params_data_list:
        if not params_data_one:
            continue
        if 'python_out' not in params_data_one and 'cnt_bad_rate' not in params_data_one:
            continue
        if 'python_out[' in params_data_one:
            continue
        params_data_one = params_data_one.replace('python_out', '').replace(' ', '').replace('"', '')
        param_data_one_list = params_data_one.split('\t')
        param_name = param_data_one_list[0].split(':')[0]
        param_bond = param_data_one_list[0].split(':')[1]
        param_good = param_data_one_list[1].split(':')[1]
        param_bad = param_data_one_list[2].split(':')[1]
        param_bad_rate = param_data_one_list[3].split(':')[1]
        param_IV = param_data_one_list[4].split(':')[1]
        params_data_dict[param_name] = dict()
        params_data_dict[param_name]['bond'] = eval(param_bond)
        params_data_dict[param_name]['good'] = eval(param_good)
        params_data_dict[param_name]['bad'] = eval(param_bad)
        params_data_dict[param_name]['bad_rate'] = eval(param_bad_rate)
        params_data_dict[param_name]['IV'] = eval(param_IV)
    return params_data_dict


def show_singe_param_pic(params_data_dict, param):
    params_data = params_data_dict.get(param)
    if params_data != None:
        y_count = [int(g_i) + int(params_data['bad'][index_g_i]) for index_g_i, g_i in enumerate(params_data['good'])]
        y_rate = [float(br_i) for br_i in params_data['bad_rate']]
        x = list(range(len(y_count)))
        ticks = ['[' + params_data['bond'][index_bd] + ',' + bd + ']' for index_bd, bd in enumerate(params_data['bond'][1:])]

        plt_show(x, ticks,y_count, y_rate, param)


def show_single(model_name, ParamsShow):
    if isinstance(ParamsShow, str):
        ParamsShow = [ParamsShow]

    if not isinstance(ParamsShow, list):
        return
    params_data_dict = get_params_data_dict(model_name)
    for param in ParamsShow:
        # if len(params_data_dict[param]['bond']) < 6:
        #     continue
        print (param)
        show_singe_param_pic(params_data_dict, param)


def show_mutil(model_name):
    params_data_dict = get_params_data_dict(model_name)
    params_data_key_valid = list(params_data_dict.keys())
    # params_data_key_valid = list(params_data_dict.keys())[:800]

    i = 0
    for param in params_data_key_valid:
        # if len(params_data_dict[param]['bond']) < 6:
        #     continue
        print (param)
        show_singe_param_pic(params_data_dict, param)
        i += 1

