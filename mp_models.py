# Code taken from 3_Speeding_Up_a_Program.ipynb in materials repository

import requests
import multiprocessing
from run_models import run_one_model, timeit, lst_to_df


session = None


def set_global_session():
    global session
    if not session:
        session = requests.Session()


@timeit
def run_models_mp(generator):
    """
    run using multiprocessing
    :param generator: generator of penalties
    :return: dataframe of coefs
    """
    with multiprocessing.Pool(initializer=set_global_session) as pool:
        coef_list = pool.map(run_one_model, generator)
    return lst_to_df(coef_list)
