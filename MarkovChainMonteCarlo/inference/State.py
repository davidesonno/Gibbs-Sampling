from itertools import product


class StatetransitionModel:
    def __init__(self, state, transitions_dict: dict):
        self.state = state
        self.dict = transitions_dict

    def nextState(self, probability):
        if probability < 0 or probability > 1:
            raise ValueError("Invalid probability")
        step = 0
        for i in range(len(self.dict.keys())):
            if probability <= self.dict[list(self.dict.keys())[i]]+step:
                return list(self.dict.keys())[i]
            step += self.dict[list(self.dict.keys())[i]]
        raise Exception("Next state not found") # should not happen


def get_transitions_model(cpds, variables, evidence=None):
    """
    returns a dict with
    keys: tuple indicating the state;
    values: StateTransitionModel object
    """

    pass


class StateCounter:
    """
    generates all the possible states given the
    possible values of each variable.
    The counter is actually a dict whose keys are a tuple
    with the values of the variables as key.
    `variables` should have the same ordering as the `values`

    Parameters
    -
    values: dict
        all possible values for each variable
    variables: list
        variables to generate the possible states for
    """
    def __init__(self, values:dict, variables:list):
        self.variables=variables # save the names
        self.values=values # save the possible values

        # gets the lists with the possible values
        aux = [values[var] for var in variables]
        combinations = list(product(*aux))
        # create the counter and initialize it 
        self.counter = {}
        for i in range(len(combinations)):
            self.counter[combinations[i]] = 0

    def update(self,next_state):
        """
        Increments the counter for `next_state`.
        The order in wich variables appear in the two dicts 
        has to be the same to work properly.
        (done with `ApproximateInference.arrange_variables()`
        in the preprocessing part of ApproximateInference.GibbsSampling)
        """
        values=tuple(next_state[var] for var in self.variables)
        self.counter[values]+=1

    def __str__(self): # could be prettier but it is quite useless
        return str(self.counter)