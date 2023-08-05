from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd
import math


class Model:
    def __init__(self, pdo=60, rate=2, base_odds=35, base_score=750,
                 card=None, combiner={}, transer=None, **kwargs):
        """

        Args:

        """
        self.lr = LogisticRegression(solver='lbfgs')
        self.pdo = pdo
        self.rate = rate
        self.base_odds = base_odds
        self.base_score = base_score

        self.factor = pdo / np.log(rate)
        self.offset = base_score - self.factor * np.log(base_odds)

        # self.combiner = combiner
        self._combiner = combiner
        self.transer = transer
        self.model = LogisticRegression(solver='lbfgs', **kwargs)

        self._feature_names = None

        if card is not None:
            # self.generate_card(card = card)
            import warnings
            warnings.warn(
                """`ScoreCard(card = {.....})` will be deprecated soon,
                    use `ScoreCard().load({.....})` instead!
                """,
                DeprecationWarning,
            )

            self.load(card)


    def fit(self, X, y):
        """
        Args:
            X (2D DataFrame)
            Y (array-like)
        """
        self.lr.fit(X, y)
        return self

    def predict(self, X, **kwargs):
        """predict score
        Args:
            X (2D array-like): X to predict
            return_sub (bool): if need to return sub score, default `False`

        Returns:
            array-like: predicted score
            DataFrame: sub score for each feature
        """
        pred_train = self.lr.predict_proba(X)[:, 1]
        return pred_train

    def export(self, X, A=363.7244, B=57.7078):
        pred_train = self.lr.predict_proba(X)[:, 1]
        X['score'] = A - B * np.log(pred_train/(1-pred_train))
        X['prob'] = pred_train
        return X


    # 将评分卡分数转换为概率
    def _score_to_prob(base_score, A, B):
        odds = math.pow(math.e, (A - base_score) / B)
        prob = odds / (1 + odds)
        return prob


