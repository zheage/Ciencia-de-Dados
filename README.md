from lightgbm import LGBMClassifier
from sklearn.base import BaseEstimator, ClassifierMixin

class LGBMBorutaWrapper(BaseEstimator, ClassifierMixin):
    def __init__(self, **kwargs):
        self.params = kwargs

    def fit(self, X, y):
        # Recria o modelo sempre que for chamado
        self.model_ = LGBMClassifier(**self.params)
        self.model_.fit(X, y)
        return self

    def predict(self, X):
        return self.model_.predict(X)

    def predict_proba(self, X):
        return self.model_.predict_proba(X)

    @property
    def feature_importances_(self):
        return self.model_.feature_importances_


from boruta import BorutaPy
import numpy as np
from sklearn.datasets import make_classification

# Criar dados simulados
X, y = make_classification(n_samples=1000, n_features=20, n_informative=5, random_state=42)

# Criar modelo encapsulado
lgbm_wrapper = LGBMBorutaWrapper(n_estimators=100, random_state=42)

# Aplicar Boruta
boruta_selector = BorutaPy(estimator=lgbm_wrapper, n_estimators='auto', verbose=2, random_state=42)
boruta_selector.fit(X, y)

# Features selecionadas
selected = boruta_selector.support_
print("Features selecionadas:", selected)
