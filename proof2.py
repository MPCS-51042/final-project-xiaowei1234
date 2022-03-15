import pandas as pd
import numpy as np
from sklearn.linear_model import PoissonRegressor, Lasso, Ridge
import statsmodels.api as sm

X_array = np.asarray([[1, 2], [1, 3], [1, 4], [1, 3]])
y = np.asarray([2, 2, 3, 2])
Preg_alpha_1 = PoissonRegressor(alpha=1., fit_intercept=False).fit(X_array, y)
print('alpha 1 Poisson Reg', Preg_alpha_1.coef_)
Preg_alpha_2 = PoissonRegressor(alpha=4., fit_intercept=False).fit(X_array*2., y)
print('alpha 2 Poisson Reg', 2. * Preg_alpha_2.coef_)
Lreg_alpha_1 = Lasso(alpha=1., fit_intercept=False).fit(X_array, y)
print('alpha 1 Lasso OLS', Lreg_alpha_1.coef_)
Lreg_alpha_2 = Lasso(alpha=2., fit_intercept=False).fit(X_array/2, y)
print('alpha 2 Lasso OLS', Lreg_alpha_2.coef_)
Rreg_alpha_1 = Ridge(alpha=1., fit_intercept=False).fit(X_array, y)
print('alpha 1 Ridge OLS', Rreg_alpha_1.coef_)
Rreg_alpha_2 = Ridge(alpha=2., fit_intercept=False).fit(X_array*4, y)
print('alpha 1 Ridge OLS', Rreg_alpha_1.coef_)


X_array_scaled = X_array.copy()
X_array_scaled[:, 1] = X_array_scaled[:, 1] * 2.

reg_alpha_scalar = PoissonRegressor(alpha=1., fit_intercept=False).fit(X_array, y)
print('scalar alpha Poisson Reg', reg_alpha_scalar.coef_)
reg_alpha_array = PoissonRegressor(alpha=[1., 4.], fit_intercept=False).fit(X_array_scaled, y)
print('array alpha Poisson Reg', reg_alpha_array.coef_)



sm_model = sm.GLM(y, X_array_scaled, family=sm.families.Poisson()).fit_regularized(alpha=[1., 4.], L1_wt=0, skip_hessian=True)
params = sm_model.params
params[1] = params[1] * 2
print ('SM scalar ridge', params)


mod_scalar = reg_alpha_scalar.fit(X_scalar/2, y)
print ('sklearn scalar', mod_scalar.coef_)

mod_array = reg_alpha_array.fit(X_array, y)
print ('sklearn array', mod_array.coef_)