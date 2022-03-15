import numpy as np
import pandas as pd
from functools import lru_cache
from sklearn.linear_model import PoissonRegressor
import statsmodels.api as sm
import time


@lru_cache(maxsize=1)
def return_X_y() -> tuple:
    """
    https://www.statsmodels.org/devel/datasets/generated/randhie.html
    :return: X, y
    """
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
    """
    decorator timeit
    :param func: the function
    :return: tuple of response and time taken
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        response = func(*args, **kwargs)
        run_time = round((time.time() - start) / 60, 3)
        return response, run_time
    return wrapper


def lst_to_df(lst_lst) -> pd.DataFrame:
    """
    iterable of iterables to pandas dataframe
    :param lst_lst: two dimensional list or array
    :return: pandas dataframe with column names
    """
    df = pd.DataFrame(lst_lst, columns=['ln coinsurance', 'num chronic diseases', 'alpha']
                      ).applymap(lambda v: round(v, 4))
    return df


@timeit
def run_models_sync(generator) -> pd.DataFrame:
    """
    synchronously run the models
    :param generator: the generator of penalty parameters
    :return: dataframe of coefficient results
    """
    model_results = []
    for alpha in generator:
        model_results.append(run_one_model(alpha))
    df = lst_to_df(model_results)
    return df
