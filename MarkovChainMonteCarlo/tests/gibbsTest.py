if __name__=='__main__':
    from pgmpy.models import BayesianNetwork
    from pgmpy.factors.discrete import TabularCPD
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

    from inference import GibbsSampling

    model = BayesianNetwork([('cloudy', 'sprinkler'), ('cloudy', 'rain'), ('sprinkler', 'wet grass'), ('rain', 'wet grass')])
    cloudy_cpd=TabularCPD('cloudy',2,[[.5],[.5]])
    sprinkler_cpd=TabularCPD('sprinkler',2,[[.5,.9],[.5,.1]],evidence=['cloudy'],evidence_card=[2])
    rain_cpd=TabularCPD('rain',2,[[.8,.2],[.2,.8]],evidence=['cloudy'],evidence_card=[2])
    grass_cpd=TabularCPD('wet grass',2,[[.99,.1,.1,.01],[.01,.9,.9,.99]],evidence=['sprinkler','rain'],evidence_card=[2,2])


    model.add_cpds(cloudy_cpd,sprinkler_cpd,rain_cpd,grass_cpd)
    # print(model.check_model())
    gibbs = GibbsSampling(model)
    q1={
        'variables':[
            'rain',
            # 'cloudy',
            'wet grass',
            # 'sprinkler'
            ],
        'evidence':{
            # 'rain':1,
            # 'cloudy':1,
            # 'wet grass':0,
            # 'sprinkler':1,
            }
    }
    print(gibbs.query(**(q1),N=10_000))
    # +-----------+---------+--------------------+
    # | cloudy    | rain    |   phi(cloudy,rain) |
    # +===========+=========+====================+
    # | cloudy(0) | rain(0) |             0.9141 |
    # +-----------+---------+--------------------+
    # | cloudy(0) | rain(1) |             0.0207 |
    # +-----------+---------+--------------------+
    # | cloudy(1) | rain(0) |             0.0464 |
    # +-----------+---------+--------------------+
    # | cloudy(1) | rain(1) |             0.0188 |
    # +-----------+---------+--------------------+

    from pgmpy.inference import VariableElimination
    inference=VariableElimination(model)
    print(inference.query(**(q1)))
    # +-----------+---------+--------------------+
    # | cloudy    | rain    |   phi(cloudy,rain) |
    # +===========+=========+====================+
    # | cloudy(0) | rain(0) |             0.9132 |
    # +-----------+---------+--------------------+
    # | cloudy(0) | rain(1) |             0.0228 |
    # +-----------+---------+--------------------+
    # | cloudy(1) | rain(0) |             0.0457 |
    # +-----------+---------+--------------------+
    # | cloudy(1) | rain(1) |             0.0183 |
    # +-----------+---------+--------------------+