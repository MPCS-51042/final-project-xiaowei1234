# Proposals
My ideas for my final project are...

1. Use Python data analysis packages such as Pandas, Numpy, and Statsmodels to measure price elasticity of grocery
items (this is from my work)

2. Create a pull request to sklearn to enable individual attribute level regularization coefficients for generalized
linear models. Currently, a scalar value is provided so that all attributes have the same regularization parameter.
The change would enable the Sklearn API to either take a scalar value or an array of numbers of equal length to
number of attributes in the model.

4. Build a flask app to output visualization of the beta distribution and output statistics for Bayesian AB testing


# Execution plan

Proposal 2 was chosen to be implemented.


By the end of the following weeks I expect to have the following finished/implemented...

Week 3 - Finished execution plan and opened issue in issue tracker in github
https://github.com/scikit-learn/scikit-learn/issues/22350

Week 4 - Finish writing functionality code as well as code documentation

Week 5 - Finish testing feature and writing unit tests

Week 6 - Aggregate all testing material and submit for review on Sklearn github

Week 7 - Create sample data analysis and simple webpage to showcase changes

Week 8 - Finish webpage and create youTube video


# Code

proof.py - comparing results of sklearn regression versus statsmodels regression using the same regularization penalties
and output to log file of comparisons

files/proof_output.log - the output of proof.py

