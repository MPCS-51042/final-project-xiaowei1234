import numpy as np
from run_models import run_models_sync
from mp_models import run_models_mp


class ModelResults:
    """
    Stores model results from synchronous or multiprocessing run
    """
    def __init__(self, df, run_time):
        self.df = df
        self.run_time = run_time

    def __repr__(self):
        """
        :return: string representation of model results
        """
        df_str_1 = f"Coefs for {self.df.columns[0]} using constant `alpha` = 1\n{list(self.df.iloc[:, 0])}"
        alpha_str = f"Alpha for num disease: {list(self.df.alpha)}"
        df_str_2 = f"Coefs for {self.df.columns[1]} using variable `alphas`\n{list(self.df.iloc[:, 1])}"
        return '\n'.join([df_str_1, alpha_str, df_str_2, f"Runtime: {self.run_time} minutes."])

    def __str__(self):
        return self.__repr__()


def make_range_gen(start, stop, incr):
    """
    generate penalties
    :param start: start
    :param stop: stop
    :param incr: step
    """
    for val in np.arange(start, stop, incr, dtype=float):
        yield val


class Database:
    """
    database
    """

    def __init__(self):
        self._data = {}

    def get(self, rng):
        if rng.alphas in self._data:
            return self._data[rng.alphas]
        return f"{rng.alphas} not found in database!"

    def put_sync(self, rng):
        gen = make_range_gen(*rng.alphas)
        coef_df, time = run_models_sync(gen)
        self._data[rng.alphas] = ModelResults(coef_df, time)

    def put_mp(self, rng):
        gen = make_range_gen(*rng.alphas)
        coef_df, time = run_models_mp(gen)
        self._data[rng.alphas] = ModelResults(coef_df, time)

    def delete_all(self):
        has = len(self._data) > 0
        self._data = {}
        return has
