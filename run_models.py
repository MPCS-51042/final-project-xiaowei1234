import numpy as np
from functools import lru_cache
from sklearn.linear_model import PoissonRegressor
import statsmodels.api as sm


@lru_cache(maxsize=1)
def return_X_y():
    data = sm.datasets.randhie.load_pandas()
    return data.exog, data.endog


@lru_cache(maxsize=None)
def run_one_model(alpha) -> np.ndarray:
    """
    runs a single model using penalties
    :param alpha: iterable of penalties or scalar value
    :return: array of coefficients
    """
    X, y = return_X_y()
    model = PoissonRegressor(alpha=alpha).fit(X, y)
    return model.coef_


def run_all_models(generator):
    pass