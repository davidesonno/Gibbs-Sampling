# I avoided adding the notations to be able to import this
def arrange_variables(values:dict, variables):
    aux=[]
    for v in list(values.keys()):
        if v in variables:
            aux.append(v)
    variables.clear()
    variables.extend(aux)

if __name__=='__main__':
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from inference import StateCounter

    values={
        'a':[0,1,2],
        'b':[1,2],
        'c':[2,3],
    }

    vars=['c','a']

    arrange_variables(values,vars)

    print(vars) # >>> ['a', 'c']

    counter=StateCounter(values,vars)
    print(counter)
    # >>> {(0, 2): 0, (0, 3): 0, (1, 2): 0, (1, 3): 0, (2, 2): 0, (2, 3): 0}

    state={
        'a':0,
        'b':1,
        'c':2,
    }

    counter.update(state) # the key (0,2) should be updated
    print(counter)
    # >>> {(0, 2): 1, (0, 3): 0, (1, 2): 0, (1, 3): 0, (2, 2): 0, (2, 3): 0}
    #              /\
    #               | 
    #               | 
    #            exactly   