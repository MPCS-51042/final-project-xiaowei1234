# Proposals
My ideas for my final project are...

1. ~~Use Python data analysis packages such as Pandas, Numpy, and Statsmodels to measure price elasticity of grocery
items (this is from my work)~~

2. Create a pull request to sklearn to enable individual attribute level regularization coefficients for generalized
linear models. Currently, a scalar value is provided so that all attributes have the same regularization parameter.
The change would enable the Sklearn API to either take a scalar value or an array of numbers of equal length to
number of attributes in the model.

4. ~~Build a flask app to output visualization of the beta distribution and output statistics for Bayesian AB testing~~


# Execution plan

Proposal 2 was chosen to be implemented.


By the end of the following weeks I expect to have the following finished/implemented...

Week 3 - Finished execution plan and opened issue in issue tracker in github
https://github.com/scikit-learn/scikit-learn/issues/22350

Week 4 - Finish writing functionality code as well as code documentation

Week 5 - Finish testing feature and writing unit tests

Week 6 - Aggregate all testing material and submit for review on Sklearn github

Week 7 - Create sample data analysis and ~~simple webpage to showcase changes~~ API

Week 8+ - Finish ~~webpage~~ API and create youTube video

# Actual project work

### 1. Sklearn pull request
Pull request was reviewed by three scikit-learn core devs and was approved but delayed due to argument over
API implementation

Pull request: https://github.com/scikit-learn/scikit-learn/pull/22485

Remote branch: https://github.com/xiaowei1234/scikit-learn/tree/glm_alpha

Sklearn issue: https://github.com/scikit-learn/scikit-learn/issues/22350

### 2. Modeling API
Creates an API that will run models according to range of regularization penalty values on one of the variables
using the RAND Health Insurance Experiment Data https://www.statsmodels.org/devel/datasets/generated/randhie.html

Able to run either synchronously or using parallel processing. Will store coefficients of a variable that has a constant penalty term of 1
and coefficients of another variable with different penalties. Will also store the run time of running the sequence of 
models with a different penalty for each.

# Code

### Sklearn pull request proofs
`proof.py` - comparing results of sklearn regression versus statsmodels regression using the same regularization penalties
and output to log file of comparisons

`files/proof_output.log` - the output of proof.py

`proof2.py` - more proof of correctness using manual calculations as suggested by sklearn devs

### API

`main.py` - the app which has `get`, two `puts` and a `delete`

`modelresults.py` - ModelResults class which stores model results from one series of penalties

`database.py` - Database class that stores all the ModelResults in a dictionary for the app

`run_models.py` - synchronously run models as well as get data and timeit functions

`mp_models.py` - use multiprocessing to run the models

`tests/test_main.py` - pytest unit tests for the app

### plot
`files/MP:_False....png` saved plot from plotting. I couldn't get plotting to work with FastAPI and was
running short on time. This is the plot produced by a unit test.