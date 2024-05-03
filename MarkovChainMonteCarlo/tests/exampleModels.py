def get_example_model(model_name="rain"):
    """
    Collection of simple models, full with CPDs.

    `model` can be:
        - "rain"
        - "earthquake"
    """
    possible_models = [
        'rain',
        'earthquake',
    ]
    if model_name not in possible_models:
        raise ValueError(
            f"Invalid name for the model\Possible models are {possible_models}")
    from pgmpy.models import BayesianNetwork
    from pgmpy.factors.discrete import TabularCPD

    if model_name == 'rain':
        rain_model = BayesianNetwork([('cloudy', 'sprinkler'), ('cloudy', 'rain'), ('sprinkler', 'wet grass'), ('rain', 'wet grass')])
        
        cloudy_cpd = TabularCPD(
                variable='cloudy', variable_card=2, 
                values=[[.5], [.5]])
        sprinkler_cpd = TabularCPD(
                variable='sprinkler', variable_card=2, 
                values=[[.5, .9], [.5, .1]], 
                evidence=['cloudy'], evidence_card=[2])
        rain_cpd = TabularCPD(
                variable='rain', variable_card=2, 
                values=[[.8, .2], [.2, .8]], 
                evidence=['cloudy'], evidence_card=[2])
        grass_cpd = TabularCPD(
                variable='wet grass', variable_card=2, 
                values=[[.99, .1, .1, .01], [.01, .9, .9, .99]], 
                evidence=['sprinkler', 'rain'], evidence_card=[2, 2])
        
        rain_model.add_cpds(cloudy_cpd, sprinkler_cpd, rain_cpd, grass_cpd)
        rain_model.check_model()
        
        return rain_model

    if model_name == 'earthquake':
        earthquake_model = BayesianNetwork([('Burglary', 'Alarm'), ('Earthquake', 'Alarm'), ('Alarm', 'JohnCalls'), ('Alarm', 'MaryCalls')])
        
        burglary_cpd = TabularCPD(
                variable='Burglary', variable_card=2, 
                values=[[0.001], [0.999]])
        earthquake_cpd = TabularCPD(
                variable='Earthquake', variable_card=2, 
                values=[[0.002], [0.998]])
        alarm_cpd = TabularCPD(
                variable='Alarm', variable_card=2, 
                values=[[0.95, 0.94, 0.29, 0.001], [0.05, 0.06, 0.71, 0.999]], 
                evidence=['Burglary', 'Earthquake'], evidence_card=[2, 2])
        johncalls_cpd = TabularCPD(
                variable='JohnCalls', variable_card=2, 
                values=[[0.90, 0.05], [0.10, 0.95]], 
                evidence=['Alarm'], evidence_card=[2])
        marycalls_cpd = TabularCPD(
                variable='MaryCalls', variable_card=2, 
                values=[[0.70, 0.01], [0.30, 0.99]], 
                evidence=['Alarm'], evidence_card=[2])
        
        earthquake_model.add_cpds(burglary_cpd, earthquake_cpd, alarm_cpd, johncalls_cpd, marycalls_cpd)
        earthquake_model.check_model()
        
        return earthquake_model

