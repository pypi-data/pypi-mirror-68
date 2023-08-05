# coding:utf-8
import os


# 建模代码目录
ROOT = os.getcwd()
# CSV 文件总目录
csvRoot = ROOT + '/Csvs/'
# 项目目录名称
projectName = 'MyProject/'
# 单个项目 CSV 目录
csvFile= csvRoot + projectName + 'CsvFile/'


# 准备入模的数据，已经完成清洗
makeModelDataFillnaFile = 'model_data_xgb_201912_lianjia_30'
ModelDataFillnaFile = 'only_model_data'


# 分箱 好坏区间及占比 IV
ruleFilePri = 'dt_rule_all'
ruleModelFilePri = 'dt_rule_model'
ruleModelFile = 'reg_rule_model'

OutModelFile = 'model_'

# 入模原始数据
scoreCardDataFile = 'model_origin_data_'
# 模型变量相关性
comParamCorrFile = 'com_param_corr_'
# 模型样本最终评分
checkDataFile = 'model_score_'
# 评分卡参数文件
scoreCardParamFile = 'score_card_param_'
# 评分卡pkl文件
scoreCardPklFile = 'score_card_pkl_'
# woe明细文件
woeFile = 'woe_'
# 是否输出woe明细文件
woe_file_output = False

# id 和 y 的变量命名
# col_head = ['cus_num', 'y']
col_head = ['employee_no', 'bad']

