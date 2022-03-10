import os
import numpy as np
from modelresults import ModelResults
from run_models import run_models_sync
from mp_models import run_models_mp
import matplotlib.pyplot as plt


class Database:
    """
    database
    """
    fig_save_loc = '/Users/xwei/repos/final-project-xiaowei1234/files'

    def __init__(self):
        self._data = {}

    def get(self, rng):
        if (rng.alphas, rng.mp) in self._data:
            return str(self._data[(rng.alphas, rng.mp)])
        return ''

    def get_image(self, rng):
        if (rng.alphas, rng.mp) not in self._data:
            return ''
        return self.make_image(self._data[(rng.alphas, rng.mp)])

    def put_db(self, rng) -> None:
        """
        put ModelResults from rng into db
        :param rng:
        :param mp: multiprocess bool
        :return: None
        """
        gen = self.make_range_gen(*rng.alphas)
        if rng.mp:
            coef_df, time = run_models_mp(gen)
        else:
            coef_df, time = run_models_sync(gen)
        self._data[(rng.alphas, rng.mp)] = ModelResults(coef_df, time, rng.mp)

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

    @staticmethod
    def make_image(model_result):
        """
        saves a figure and also returns the image in bytes
        :param model_result: saved model result
        :return: image in bytes
        """
        mr = model_result
        title = f"MP: {mr.multiprocess}, Alpha: {mr.df.alpha.min()} to {mr.df.alpha.max()}, Runtime: {mr.run_time}"
        file_title = title.replace(' ', '_')
        # fig = mr.df.set_index('alpha').plot(kind='line', legend=True, figsize=(8, 6), title=title
        #                                     , xlabel='alpha for num chronic diseases').get_figure()
        fig = plt.figure(figsize=(8, 6))
        x = mr.df.alpha
        y = mr.df['ln coinsurance']
        y2 = mr.df['num chronic diseases']
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(x, y)
        ax.plot(x, y2)
        fig.savefig(os.path.sep.join([Database.fig_save_loc, f'{file_title}.png']))
        return fig
