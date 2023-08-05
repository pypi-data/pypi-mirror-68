# coding:utf-8

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, _tree
from sklearn.metrics import roc_auc_score,roc_curve,auc
from sklearn.model_selection import train_test_split
from .utils import fillna, bin_by_splits, to_ndarray, clip
from .utils.decorator import support_dataframe

DEFAULT_BINS = 10
DEFAULT_DECIMAL = 4 # 默认小数精度


def DTMerge(feature, target, nan = -1, n_bins = None, min_samples = 1):
    """Merge by Decision Tree

    Args:
        feature (array-like)
        target (array-like): target will be used to fit decision tree
        nan (number): value will be used to fill nan
        n_bins (int): n groups that will be merged into
        min_samples (int): min number of samples in each leaf nodes

    Returns:
        array: array of split points
    """
    if n_bins is None and min_samples == 1:
        n_bins = DEFAULT_BINS

    feature = fillna(feature, by = nan)

    tree = DecisionTreeClassifier(
        min_samples_leaf = min_samples,
        max_leaf_nodes = n_bins,
    )
    tree.fit(feature.reshape((-1, 1)), target)

    thresholds = tree.tree_.threshold
    thresholds = thresholds[thresholds != _tree.TREE_UNDEFINED]

    # 结果取4位小数
    for i in range(len(thresholds)):
        if type(thresholds[i]) == np.float64:
            thresholds[i] = round(thresholds[i],DEFAULT_DECIMAL)

    return np.sort(thresholds)


@support_dataframe(require_target = False)
def merge(feature, target = None, method = 'dt', return_splits = False, **kwargs):
    """merge feature into groups

    Args:
        feature (array-like)
        target (array-like)
        method (str): 'dt', 'chi', 'quantile', 'step', 'kmeans' - the strategy to be used to merge feature
        return_splits (bool): if needs to return splits
        n_bins (int): n groups that will be merged into


    Returns:
        array: a array of merged label with the same size of feature
        array: list of split points
    """
    feature = to_ndarray(feature)
    method = method.lower()

    # if method == 'dt':
    #     splits = DTMerge(feature, target, **kwargs)
    # else:
    #     splits = np.empty(shape = (0,))
    #目前仅支持决策树分箱
    splits = DTMerge(feature, target, **kwargs)


    if len(splits):
        bins = bin_by_splits(feature, splits)
    else:
        bins = np.zeros(len(feature))

    if return_splits:
        return bins, splits

    return bins


