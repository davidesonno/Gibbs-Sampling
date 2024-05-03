from pgmpy.inference import VariableElimination
from pgmpy.models import BayesianNetwork
from random import uniform, choice


class MCMC(BayesianNetwork):
    def __init__(self, model):
        model.check_model()
        self.model = model
        self.cpds = model.cpds
        self.cardinalities = dict(model.get_cardinality())
        self.variable_values = {
            cpd.variable: cpd.state_names[cpd.variable] for cpd in model.get_cpds()}

    def query(
            self,
            variables,
            evidence=None,
            N=10_000
    ):
        from inference.State import get_transitions_model
        """old"""
        # evidence = evidence if evidence is not None else dict()
        # # used to return the query
        # used_variables = [v for v in variables]+[k for k in evidence.keys()]
        # # using the possible values of th evariables,
        # # initiate a state considering the evidence
        # initial_state = self.cardinalities.copy()
        # for k in initial_state.keys():
        #     if k in evidence.keys():
        #         initial_state[k] = evidence[k]
        #     else:
        #         initial_state[k] = random.randint(0, initial_state[k]-1)
        # # generates the possible states
        # encodings = self.gen_encode_dict(self.variable_values,used_variables)
        # print(encodings)
        # # start sampling
        # for _ in range(N):

        """new """
        # used_variables = [v for v in variables]+[k fo   r k in evidence.keys()]
        transitions = get_transitions_model(self.cpds, variables, evidence)
        # return QueryResult(variables, encode)


class GibbsSampling:
    """
    Parameters
    -
    model: pgmpy.models.BayesianNetwork
    """

    def __init__(self, model):
        if not isinstance(model, BayesianNetwork):
            raise ValueError("The model is not a pgmpy Bayesian Network")
        model.check_model()  # checks cpds
        self.model = model
        self.cpds = model.cpds  # saves cpds
        # the possible values for each node
        self.variable_values = {
            cpd.variable: cpd.state_names[cpd.variable] for cpd in self.cpds}
        # precompute the blankets
        self.blankets = {
            var: self.model.get_markov_blanket(var)
            for var in self.variable_values.keys()
        }

    def query(
            self,
            variables,
            evidence=None,
            virtual_evidence=None,          # unused
            elimination_order="greedy",     #
            joint=True,                     #
            show_progress=True,             #
            N=100_000,
            rounding=4
    ):
        """
        Execute the approximate inference using the Gibbs Algorithm.

        Parameters
        -
        variables: list
            list of variables for which you want to compute the probability

        evidence: dict
            a dict, (key, value) pair as {var: state_of_var_observed}
            None if no evidence

        rounding: int 
            optional parameter to be able to print smaller 
            probabilities

        virtual_evidence, elimination_order, joint, show_progress:
            unused, they are here solely for portability with the `query`
            method of `pgmpy.inference`
        """
        from inference.State import StateCounter
        from query import QueryResult
        from math import ceil
        # in theory variables exceptions are already covered by pgmpy...
        self.check_variables(variables)  # still lets check them
        # check the values of evidence
        if evidence is not None:
            self.check_evidence(evidence)
        else:
            evidence = dict()
        if N < 1:
            raise ValueError(
                "Number of iterations has to be greater than zero")
        # ensure the order of `variables` is the same as in `self.variable_values`
        arrange_variables(self.variable_values, variables)

        # initiate a random state considering the evidence
        current_state = self.variable_values.copy()
        for var in current_state.keys():
            if var in evidence.keys():
                current_state[var] = evidence[var]
            else:
                current_state[var] = choice(self.variable_values[var])
        # choose the visiting order for the variables
        ordering = [var for var in self.variable_values.keys()
                    if var not in evidence.keys()]
        # generates the possible states for `variables`
        state_counter = StateCounter(self.variable_values, variables)
        # start sampling
        for _ in range(ceil(N/len(ordering))):
            for var in ordering:
                # generate from Uniform(0,1) and use variable elimination
                # to compute P(var|blanket(var))
                current_evidence = {
                    ce: current_state[ce] for ce in self.blankets[var]}
                query = VariableElimination(self.model).query(
                    [var], current_evidence).values
                next_value_index = read_distribution(query, uniform(0, 1))
                # update current state
                current_state[var] = self.variable_values[var][next_value_index]
                state_counter.update(current_state)

        # return the query
        return QueryResult(state_counter, rounding)

    def check_evidence(self, evidence):
        for e in list(evidence.keys()):
            if evidence[e] not in self.variable_values[e]:
                raise ValueError(
                    f"Invalid state for {e}; possible states: {self.variable_values[e]}")

    def check_variables(self, variables):
        for var in variables:
            if var not in list(self.variable_values.keys()):
                raise ValueError(
                    f"The variable {var} is not part of the model")


def read_distribution(query, probability:float):
    """
    Returns the index value associated with the given probability

    Parameters
    -
    query: nparray
        nparray containing the distribution of a query

    probability: float
    """
    step = 0
    for i in range(len(query)):  # will always be 1-D
        if probability <= query[i]+step:
            return i
        step += query[i]
    raise Exception("Next state not found or probability greater than 1")  # should not happen...


def arrange_variables(values: dict, variables:iter):
    """
    Takes a dict of the values for all the variables and
    re-arranges `variables` in-place according to the order of the keys
    """
    aux = []
    for v in list(values.keys()):
        if v in variables:
            aux.append(v)
    variables.clear()
    variables.extend(aux)
