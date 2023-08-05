# coding:utf-8

import os
import time
from lapras.Settings import makeModelDataFillnaFile, ModelDataFillnaFile, ruleModelFilePri, ruleModelFile, OutModelFile
from lapras.Settings import csvFile, ruleFilePri, scoreCardDataFile, comParamCorrFile, checkDataFile,scoreCardParamFile,scoreCardPklFile,woeFile
from lapras.ReportConfig import cut_points_step, assist_num, score_bond
from lapras.ModelConfig import A, B, eps
from lapras.ReportConfig import ParamsShow, ModelName
from lapras.report.ReportConfigUtil import get_param_bond_woe_all_theta, get_GBK_Name

# 文件部分

if not os.path.exists(csvFile):
    os.makedirs(csvFile)
# 全部变量的 csv数据文件
makeModelDataFillnaFileName = csvFile + makeModelDataFillnaFile + '.csv'
# 只有入模变量的 csv 文件
OnlyModelDataFillnaFileName = csvFile + ModelDataFillnaFile + '.csv'


# 分箱 好坏区间及占比 IV
# 全量
ruleFilePriName =  csvFile + ruleFilePri + '.csv'
# 只看入模变量的
# 决策树分
ruleModelFilePriName =  csvFile + ruleModelFilePri + '.csv'
# 手动分
ruleModelFileName =  csvFile + ruleModelFile + '.csv'


OutModelFileName =  csvFile + OutModelFile + time.strftime("%Y%m%d_%H%M%S", time.localtime())


#  当前入模变量的 csv数据文件
scoreCardDataFileName =  csvFile + scoreCardDataFile + 'file' + '.csv'
# 模型变量相关性
comParamCorrFileName =  csvFile + comParamCorrFile + 'file' + '.csv'
# 模型变量评分
checkDataFileName =  csvFile + checkDataFile + 'file' + '.csv'
# 评分卡参数文件
scoreCardParamFileName =  csvFile + scoreCardParamFile + 'file' + '.txt'
# 评分卡pkl文件
scoreCardPklFileName =  csvFile + scoreCardPklFile + 'file' + '.pkl'
# woe明细文件路径
woeFileName =  csvFile + woeFile + 'file' + '.csv'



# 生成报告需要的模型文件
# 单变量分析的model文件， 主要用于模型单变量查看
singleModelName = csvFile + ModelName

try:
    with open(singleModelName, 'r') as f:
        params_data = f.read()
    f.close()
    params, param_bond, woe_all, theta, bond_list = get_param_bond_woe_all_theta(params_data)
except:
    params, param_bond, woe_all, theta, bond_list = (0, 0, 0, 0, 0)


