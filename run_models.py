import numpy as np
import pandas as pd
from functools import lru_cache
from sklearn.linear_model import PoissonRegressor
import statsmodels.api as sm
import time


@lru_cache(maxsize=1)
def return_X_y() -> tuple:
    data = sm.datasets.randhie.load_pandas()
    return data.exog, data.endog


#@lru_cache(maxsize=None)
def run_one_model(alpha) -> np.ndarray:
    """
    runs a single model using penalties
    :param alpha: iterable of penalties or scalar value
    :return: array of coefficients
    """
    X, y = return_X_y()
    alphas = [1.] * 5 + [alpha] + [1.] * 3
    model = PoissonRegressor(alpha=alphas).fit(X, y)
    return np.hstack((model.coef_[[0, 5]], alpha))


def timeit(func):

    def wrapper(*args, **kwargs):
        start = time.time()
        response = func(*args, **kwargs)
        run_time = round((time.time() - start) / 60, 4)
        return response, run_time
    return wrapper


def lst_to_df(lst_lst):
    df = pd.DataFrame(lst_lst, columns=['ln coinsurance', 'num chronic diseases', 'alpha']).applymap(lambda v: round(v, 2))
    return df


@timeit
def run_models_sync(generator):
    model_results = []
    for alpha in generator:
        model_results.append(run_one_model(alpha))
    df = lst_to_df(model_results)
    return df
