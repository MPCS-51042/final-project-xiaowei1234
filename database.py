import run_models as rm
import statsmodels.api as sm


class Database:
    """
    database
    """
    X, y = return_X_y()

    def __init__(self):
        self._data = {}

    def get(self, key):
        return self._data[key]

    def put(self, key, value):
        coefs = rm.run_all_models(range(*value))
        self._data[key] = coefs

    def all(self):
        return self._data

    def delete_all(self):
        self._data = {}
