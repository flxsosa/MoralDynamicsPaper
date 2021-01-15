import moral_kinematics_scenarios as scenarios

def determine_outcome(environment):
    '''
    Determines whether a collision occurs within a simulation between
    a Patient and Fireball.
    '''
    environment.run()
    return environment.patient_fireball_collision, environment.agent_patient_collision

def run_sim(environment):
    environment = environment(False)
    environment.run()
    return environment.agent.effort_expended

def counterfactual_simulation(true_outcome,environment,tick,std_dev,num_times):
    # Determine counterfactual probability
    # TODO: Cancel counterfactual simulations if there is no agent-patient
    #   collision
    counterfactual_prob = 0.0
    for _ in range(num_times):
        env = environment(False)
        # Run the counterfactual simulation
        env.counterfactual_run(std_dev,tick)
        # Determine outcome
        counterfactual_outcome = env.patient_fireball_collision
        counterfactual_prob += int(true_outcome == counterfactual_outcome)
    return counterfactual_prob / num_times

def iterate_std_dev(environment,start,end,step,num_times):
    # Retrieve true oucome of simulation w/o noise
    true_outcome, collision_tick = determine_outcome(environment(False))
    std_dev_prob_map = {}
    for std_dev in range(start,end,step):
        counterfactual_prob = counterfactual_simulation(true_outcome,
                                                        environment,
                                                        collision_tick,
                                                        std_dev,num_times)
        std_dev_prob_map[std_dev] = counterfactual_prob
    return std_dev_prob_map

# for scene in scenarios.__experiment3__:
#     print("==== Simulation ==== ", scene)
#     sim = getattr(scenarios, scene)
#     m = iterate_std_dev(sim,start=10,end=110,step=10,num_times=100)
#     print("   ", m)

for scene in scenarios.__experiment3__:
    print("==== Simulation ==== ", scene)
    sim = getattr(scenarios, scene)
    m = run_sim(sim)
    print(m)
