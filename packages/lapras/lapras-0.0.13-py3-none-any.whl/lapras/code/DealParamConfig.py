# coding:utf-8

from lapras.ModelConfig import bin_params_dict
from lapras.ModelConfig import  minLeaf, treeDepth, bucketnum

params = list(bin_params_dict.keys())
bin_params =  [bin_params_dict.get(para) for para in params]