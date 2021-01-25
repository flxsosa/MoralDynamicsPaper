'''
Execute and record values from scenarios.

Felix Sosa
March 8, 2018
'''
import matplotlib.pyplot as plt
import csv
from importlib import import_module
from counterfactual import iterate_std_dev
import pandas as pd

# Import the scenario file and store them in a variable
scenarios = import_module('moral_kinematics_scenarios')

def write_results(filename,scenarios,effort_vals,causal_vals):
	exp_results = open(filename+".csv",'w')
	keys = scenarios
	writer = csv.DictWriter(exp_results,fieldnames=['scenario','effort','causality'])
	writer.writeheader()
	for i in range(len(scenarios)):
		writer.writerow({'scenario':scenarios[i],
				 'effort':effort_vals[i],
				 'causality':causal_vals[i]})
	exp_results.close()
def record(scenarios,library=scenarios):
	effort_vals=[]
	s = []
	c = []
	avg = lambda x: sum(list(x.values()))/len(list(x.values()))
	for scenario_name in scenarios:
		scene = getattr(library,scenario_name)
		t_scene = scene(False)
		t_scene.run()
		causality = iterate_std_dev(scene,start=0.1,end=2.1,step=0.1,num_times=100)
		effort_vals.append(t_scene.agent.effort_expended)
		c.append(avg(causality))
		s.append(scenario_name)
	return effort_vals, s, c

# exp1_effort_values, exp1_scenarios,e1_c = record(scenarios.__experiment1__)
# exp2_effort_values, exp2_scenarios,e2_c = record(scenarios.__experiment2__)
# exp3_effort_values, exp3_scenarios,e3_c = record(scenarios.__experiment3__)
# write_results('exp1results',scenarios.__experiment1__,exp1_effort_values,e1_c)
# write_results('exp2results',scenarios.__experiment2__,exp2_effort_values,e2_c)
# write_results('exp3results',scenarios.__experiment3__,exp3_effort_values,e3_c)
data = pd.read_csv('exp3results.csv')
uncertain = data.loc[[14,15,2,3,10,13,9,12]]
causal = data.loc[[5,6,7,11,8,20,4]]
noncausal = data.loc[[18,19,0,1,16,17]]
uncertain_corr = uncertain['effort'].corr(uncertain['causality'])
causal_corr = causal['effort'].corr(causal['causality'])
noncausal_corr = noncausal['effort'].corr(noncausal['causality'])
corr_ = data['effort'].corr(data['causality'])
print(corr_)
print(uncertain_corr)
print(causal_corr)
print(noncausal_corr)

import seaborn as sns
sns.lmplot(x='effort',y='causality',data=noncausal)
plt.show()
sns.lmplot(x='effort',y='causality',data=causal)
plt.show()
