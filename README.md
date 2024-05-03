This project will discuss the implementation of an algorithm to compute approximate inference for Bayesian Networks: the Gibbs Sampling.

The method for computing approximate inference is an instance of Markov Chain Monte Carlo algorithms, a simulation approach that, using the convergence property of the Markov Chains, computes the desired probability.

We are going to use this method on networks created with the _pgmpy_ library and through the class _Gibbs Sampling_ we can query some distributions over the model, given some evidence.
