import pandas as pd
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
    with multiprocessing.Pool(initializer=set_global_session) as pool:
        coef_list = pool.map(run_one_model, generator)
    return lst_to_df(coef_list)
