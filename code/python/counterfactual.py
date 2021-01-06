import moral_kinematics_scenarios as scenarios

def determine_outcome(environment):
    '''
    Determines whether a collision occurs within a simulation between
    a Patient and Fireball.
    '''
    return environment.patient_fireball_collision, environment.agent_collision

def counterfactual_simulation(true_outcome, environment,std_dev,num_times):

    # Determine counterfactual probability
    counterfactual_prob = 0.0
    for _ in range(num_times):
        # Run the counterfactual simulation
        counterfactual_env = environment(view=True, std_dev=std_dev)
        # Determine outcome
        counterfactual_outcome = determine_collision(counterfactual_env)
        counterfactual_prob += int(true_outcome == counterfactual_outcome)
    return counterfactual_prob / num_times

def iterate_std_dev(environment, start, end, step, num_times):
    # Retrieve true oucome of simulation w/o noise
    true_outcome, collision_tick = determine_outcome(environment(True,0))
    std_dev_prob_map = {}
    for std_dev in range(start,end,step):
        counterfactual_prob = counterfactual_simulation(true_outcome, environment, std_dev, num_times)
        std_dev_prob_map[std_dev] = counterfactual_prob
    return std_dev_prob_map

for scene in scenarios.__test__:
    sim = getattr(scenarios, scene)
    m = iterate_std_dev(sim, 0,1,1,1)
    print(scene)
    print(m)
