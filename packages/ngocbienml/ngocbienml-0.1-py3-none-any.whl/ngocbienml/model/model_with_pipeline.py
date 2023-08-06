from sklearn.base import BaseEstimator, TransformerMixin

import gc
from time import time

from ..utils.config import *
from ..visualization.plot import Plot
from sklearn.model_selection import train_test_split
from ..utils.utils_ import *
from ..metrics.metrics_ import binary_score, multiclass_score
import lightgbm as lgb


params = {'feature_fraction': 0.7319044104939286,
          'max_depth': 65,
          'min_child_weight': 1e-05,
          'min_data_in_leaf': 47,
          'n_estimators': 497,
          'num_leaves': 45,
          'reg_alpha': 0,
          'reg_lambda': 50,
          'metric': 'auc',
          'eval_metric': 'auc',
          'is_unbalance': True,
          'subsample': 0.5380272330885912}


class ModelWithPipeline(BaseEstimator, TransformerMixin):

    def __init__(self):

        self.model = lgb.LGBMClassifier(**params)

    def fit(self, X, y=None, **kwargs):
        print('Input data to trainning has shape=', X.shape)
        assert len(X)==len(y)
        print('split data in train, test by 80:20')
        X1,  X2, y1, y2 = train_test_split(X, y, random_state=49, test_size=.2, stratify=y)
        print('start to training model by LGBClassifier...')
        self.model.fit(X1, y1, eval_set=[(X1, y1), (X2, y2)], verbose=-1)
        binary_score(self.model, X1, y1, name='train')
        binary_score(self.model, X2, y2, name='test')
        self.plot(X)
        return self

    def plot(self, X):

        plot_ = Plot(name="LGB classifier",
                     model=self.model,
                     feat_name = X.columns,
                     lgb = lgb)
        plot_.plot_metric_and_importance()
        return self

    def predict(self, X, **kwargs):
        return self.model.predict(X)

    def predict_proba(self, X, **kwargs):
        return self.model.predict_proba(X)

    def score(self, X, y=None):

        binary_score(self.model, X, y, name='extrat test')
        return self
