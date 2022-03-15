import os
import sys
import logging
import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import PoissonRegressor

if not os.path.isdir('./files'):
    os.mkdir('./files')

logging.basicConfig(filename='./files/proof_output.log', encoding='utf-8', level=logging.INFO, filemode='w')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


logging.info('data source: ' 'https://www.statsmodels.org/devel/datasets/generated/randhie.html')
data = sm.datasets.randhie.load_pandas()


def list_to_str(lst, places=4):
    lst = [str(round(f, places)) for f in lst]
    return '(' + ', '.join(lst) + ')'


def run_sk_reg(alpha, dataset, log=True):
    reg = PoissonRegressor(alpha=alpha).fit(dataset.exog, dataset.endog)
    coefs = list(reg.coef_)
    if log:
        logging.info('Sklearn coefs: ' + list_to_str(coefs))
    return coefs


def run_sm_reg(alpha, dataset, log=True):
    model = sm.GLM(dataset.endog, sm.add_constant(dataset.exog), family=sm.families.Poisson())
    alpha_array = [0.] + list(alpha) if hasattr(alpha, '__iter__') else [0.] + [alpha] * dataset.exog.shape[1]
    reg = model.fit_regularized(alpha=alpha_array, L1_wt=0, skip_hessian=True)#)
    coefs = list(reg.params.values[1:])
    if log:
        logging.info('Statsmodels coefs:' + list_to_str(coefs))
    return coefs


logging.info('\nalpha = 0.')
run_sm_reg(0., data)
run_sk_reg(0., data)

logging.info('\nalpha = 1.')
run_sk_reg(1., data)
run_sm_reg(1., data)

logging.info('\nalpha = [.1] * 9')
alphas = [0.1] * 9
run_sk_reg(alphas, data)
run_sm_reg(alphas, data)

logging.info('\nalpha = [2.] + [.1] * 8')
alphas = [2.] + [.1] * 8
run_sk_reg(alphas, data)
run_sm_reg(alphas, data)

n_rand_test = 100

logging.info(f'\nRunning {n_rand_test} regressions using random weights and raise error if difference between'
             ' sklearn and statsmodels is more than two decimal places')

np.random.seed(3)
max_diffs = []
for i in range(n_rand_test):
    rand_alphas = np.random.rand(9)
    sk_coefs = run_sk_reg(rand_alphas, data, False)
    sm_coefs = run_sm_reg(rand_alphas, data, False)
    np.testing.assert_array_almost_equal(sk_coefs, sm_coefs, decimal=2)
    max_diff = np.max(np.abs(np.asarray(sk_coefs) - np.asarray(sm_coefs)))
    max_diffs.append(max_diff)

logging.info(f'\nArrays are equal to 2 decimal places in {n_rand_test} random trials')

maximum = np.max(max_diffs)
logging.info(f'\nMax absolute difference between coefficients in {n_rand_test} is: {maximum}')

logging.info(f'\nList of max abs difference for the {n_rand_test} random alpha arrays' + list_to_str(max_diffs, places=6))

logging.info('\nAny difference in estimations may be due to optimization method in sklearn uses lbfgs'
             ' while Statsmodels uses bfgs')