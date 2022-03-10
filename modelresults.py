class ModelResults:
    """
    Stores model results from synchronous or multiprocessing run
    """
    def __init__(self, df, run_time: float, multiprocess: bool):
        """
        :param df: dataframe with column names ['ln coinsurance', 'num chronic diseases', 'alpha']
        :param run_time: run time in minutes
        """
        self.df = df
        self.run_time = run_time
        self.multiprocess = multiprocess

    def __repr__(self):
        """
        :return: string representation of model results
        """
        mp_str = f"Multiprocessing: {self.multiprocess}"
        df_str_1 = f"Coefs for {self.df.columns[0]} using constant `alpha` = 1\n{list(self.df.iloc[:, 0])}"
        alpha_str = f"Alpha for num disease: {list(self.df.alpha)}"
        df_str_2 = f"Coefs for {self.df.columns[1]} using variable `alphas`\n{list(self.df.iloc[:, 1])}"
        return '\n'.join([mp_str, df_str_1, alpha_str, df_str_2, f"Runtime: {self.run_time} minutes."])

    def __str__(self):
        return self.__repr__()
