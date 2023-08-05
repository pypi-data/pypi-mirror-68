# coding:utf-8

import numpy as np
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
import re

def decisionTreeSplit(datax, datay, DepthOfTree, MinSamplesLeaf):
    groupdt = DecisionTreeClassifier(criterion='entropy', splitter='best', max_depth=DepthOfTree,
                                     min_samples_leaf=MinSamplesLeaf)
    groupdt.fit(datax.reshape((datax.shape[0], 1)), datay.reshape((datay.shape[0], 1)))
    dot_data = tree.export_graphviz(groupdt, out_file=None, )
    pattern = re.compile('<= (.*?)\\\\nentropy', re.S)
    split_num = re.findall(pattern, dot_data)
    a = [float(b) for b in split_num]
    return sorted(a)

