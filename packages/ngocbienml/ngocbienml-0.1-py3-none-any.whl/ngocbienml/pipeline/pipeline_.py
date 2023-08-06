from sklearn.pipeline import Pipeline
from ..data_processing import Fillna, LabelEncoder, FillnaAndDropCatFeat, MinMaxScale, FeatureSelection
from ..model import ModelWithPipeline
from ..metrics import binary_score_

STEPS = [('fillna', Fillna()),
        ('label_encoder', LabelEncoder()),
        ('FillnaAndDropCat', FillnaAndDropCatFeat()),
        ('MinMaxScale', MinMaxScale()),
        ('FeatureSelection', FeatureSelection()),
        ('classification', ModelWithPipeline())]


class MyPipeline:

    def __init__(self,  steps=STEPS):
        self.steps = steps
        self.pipeline_ = Pipeline(steps=self.steps)

    def fit(self, X, y=None):
        print('start to using pipeline to fit data. Data shape=', X.shape)
        self.pipeline_.fit(X=X, y=y)
        return self

    def transform(self, X, y=None):
        return self.pipeline_.transform(X, y=y)

    def score(self, X, y=None):
        y_label = self.pipeline_.predict(X)
        y_proba = self.pipeline_.predict_proba(X)
        binary_score_(y, y_label, y_proba)
        return self
