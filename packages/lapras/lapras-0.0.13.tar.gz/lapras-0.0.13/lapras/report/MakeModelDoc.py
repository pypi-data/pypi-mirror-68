# coding:utf-8



import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from collections import Counter
from lapras.ReportConfig import x_label, y_label_left, y_label_right, graph_title, line_flag

'''
制作 模型部署文档 的准备部分，准备变量和对应模型分

需要  config 或 settings 中 含有 params, theta, woe_all, param_bond
需要  config  或 setting 中 含有 B, score_bond check_data_storeout（文件）
需要  文件check_data_storeout 中包含 y 和 score 即样本表现和样本评分
'''

def get_max_int(int_data):
    return int(str(int(str(int_data)[0])+1) + '0' * (len(str(int_data))-1))

def count_point(frame, score_bond, score='score', target='bad'):
    '''
    读取分数文件 包含 y base_score 字段
    y 为表现 base_score 为 评分
    :return: 各区间好坏样本数量
    '''
    scoredata = frame
    labels = list(range(len(score_bond) - 1))
    baddf = scoredata[scoredata[target] == 1]
    gooddf = scoredata[scoredata[target] == 0]

    # 获得 好坏样本 总样本
    badstat = pd.cut(baddf[score], bins=score_bond, labels=labels, include_lowest=True)
    goodstat = pd.cut(gooddf[score], bins=score_bond, labels=labels, include_lowest=True)
    allstat = pd.cut(scoredata[score], bins=score_bond, labels=labels, include_lowest=True)

    # 统计各分数段样本数量
    badstat_result = pd.value_counts(badstat, sort=False)
    goodstat_result = pd.value_counts(goodstat, sort=False)
    allstat_result = pd.value_counts(allstat, sort=False)

    bad_count = badstat_result.tolist()
    good_count = goodstat_result.tolist()
    y_count = allstat_result.tolist()
    print('bad: %s' % bad_count)
    print('good: %s' % good_count)
    print('all: %s' % y_count)
    all_rate = ['%.2f%%'%(y_c/sum(y_count) *100) for y_c in y_count]
    print('all_rate: %s' % all_rate)


    # 计算区间坏账率
    ticks =  ['(%d,%d]' % (score_bond[i], score_bond[i+1]) for (i,x) in enumerate(score_bond) if i<len(score_bond)-1]
    score_stat_df = pd.DataFrame({'labels':labels,'bad_count':bad_count,'good_count':good_count,'y_count':y_count})
    # score_stat_df['ratio'] = score_stat_df['bad_count']/(score_stat_df['good_count']+score_stat_df['bad_count'])
    score_stat_df['y_rate'] = score_stat_df['bad_count']/(score_stat_df['y_count'])
    # score_stat_df['ratio'] = score_stat_df['bad_count']/len( score_stat_df['bad_count'])
    x = score_stat_df['labels']
    y_rate = score_stat_df['y_rate']
    y_rate_cent = ['%.2f%%'%(y_i *100) for y_i in list(y_rate)]
    print ('bad_rate: %s'%(y_rate_cent))
    base_score_count = Counter(list(scoredata[score]))
    print ('重复分重复次数排序（前15个） %s'%base_score_count.most_common()[:15])
    # x: 区间分段 1,2,3,4
    # ticks: 区间名称['[300, 400)', '[400, 500)',  '[500, 1000)']
    # y_count: 区间 数量， 表示评分在此区间内的样本数量
    # y_rate: 区间 坏账率
    return x, ticks, y_count, y_rate

def plt_show(x, ticks,y_count, y_rate, title=None):
    '''
    画 柱状图 和 折线图
    :param x: 区间分段 1,2,3,4
    :param ticks: 区间名称['[300, 400)', '[400, 500)',  '[500, 1000)']
    :param y_count: 区间 数量， 表示评分在此区间内的样本数量
    :param y_rate: 区间 坏账率
    '''
    # 设置字体、图形样式
    # sns.set_style("whitegrid")
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['font.family'] = 'sans-serif'
    matplotlib.rcParams['axes.unicode_minus'] = False
    matplotlib.fontsize='15'

    y1 = y_count
    y2 = y_rate
    # 设置图形大小
    plt.rcParams['figure.figsize'] = (18.0, 9.0)

    fig = plt.figure()

    # 画柱子
    ax1 = fig.add_subplot(111)
    # alpha透明度， edgecolor边框颜色，color柱子颜色 linewidth width 配合去掉柱子间距
    ax1.bar(x, y1, alpha=0.8, edgecolor='k', color='#836FFF',linewidth=1, width =1)
    # 获取 y 最大值 最高位 + 1 的数值 比如 201取300，320取400，1800取2000
    y1_lim = get_max_int(max(y1))
    # 设置 y轴 边界
    ax1.set_ylim([0, y1_lim])
    # 设置 y轴 标题
    ax1.set_ylabel(y_label_left, fontsize='15')
    ax1.set_xlabel(x_label,fontsize='15')
    # 将分值标注在图形上
    for x_i, y_i in  zip(x, y1):
        ax1.text(x_i, y_i + y1_lim/20, str(y_i), ha='center', va='top', fontsize=13, rotation=0)

    # 设置标题
    if title != None:
        ax1.set_title(title, fontsize='20')
    else:
        ax1.set_title(graph_title, fontsize='20')
    plt.yticks(fontsize=15)
    # plt.xticks(x, y)
    plt.xticks(fontsize=12)

    # 画折线图
    if line_flag:
        ax2 = ax1.twinx()  # 这个很重要噢
        ax2.plot(x, y2, 'r', marker='*', ms=0)

        # ax2.set_xlim([-0.5, 3.5])
        try:
            y2_lim = (int(max(y2) * 10) + 1) / 10
        except:
            y2_lim = 1
        ax2.set_ylim([0, y2_lim])
        ax2.set_ylabel(y_label_right, fontsize='15')
        ax2.set_xlabel(x_label,fontsize='15')
        for x_i, y_i in  zip(x, y2):
            ax2.text(x_i, y_i+y2_lim/20 , '%.2f%%'%(y_i *100), ha='center', va='top', fontsize=13, rotation=0)
    plt.yticks(fontsize=15)
    plt.xticks(x, ticks)
    plt.xticks(fontsize=15)

    # 是否显示网格
    plt.grid(True)

    # 保存图片 dpi为图像分辨率
    # plt.savefig('分数分布及区间坏账率.png', dpi=600, bbox_inches='tight')
    # 显示图片
    plt.show()

