import numpy as np
from modelresults import ModelResults
from run_models import run_models_sync
from mp_models import run_models_mp


class Database:
    """
    database
    """

    def __init__(self):
        self._data = {}

    def get(self, rng):
        if rng.alphas in self._data:
            return str(self._data[rng.alphas])
        return ''

    def put_sync(self, rng):
        gen = self.make_range_gen(*rng.alphas)
        coef_df, time = run_models_sync(gen)
        self._data[rng.alphas] = ModelResults(coef_df, time)

    def put_mp(self, rng):
        gen = self.make_range_gen(*rng.alphas)
        coef_df, time = run_models_mp(gen)
        self._data[rng.alphas] = ModelResults(coef_df, time)

    def delete_all(self):
        has = len(self._data) > 0
        self._data = {}
        return has

    @staticmethod
    def make_range_gen(start, stop, incr):
        """
        generate penalties
        :param start: start
        :param stop: stop
        :param incr: step
        """
        for val in np.arange(start, stop, incr, dtype=float):
            yield val
