'''
Execute and record values from scenarios.

Felix Sosa
March 8, 2018
'''
import matplotlib.pyplot as plt
import csv
from importlib import import_module

# Import the scenario file and store them in a variable
scenarios = import_module('moral_kinematics_scenarios')

# List for effort values and scenario names for recording into a CSV
exp1_effort_values = []
exp1_scenarios = []
exp2_effort_values = []
exp2_scenarios = []

# Run scenarios and record the effort values from the Blue agent
for scenario_name in scenarios.__experiment1__:
	scenario = getattr(scenarios, scenario_name)
	exp1_effort_values.append(scenario(False)) # Flip this to True to view
	exp1_scenarios.append(scenario.__name__)

# Run scenarios and record the effort values from the Blue agent
for scenario_name in scenarios.__experiment2__:
	scenario = getattr(scenarios, scenario_name)
	exp2_effort_values.append(scenario(False)) # Flip this to True to view
	exp2_scenarios.append(scenario.__name__)

# Write scenario results (effort values for Blue agent) from scenarios in 
# experiment 1 to a CSV file
exp1_results_csv = open('../../data/model/experimenta.csv','w')
keys = exp1_scenarios
writer = csv.DictWriter(exp1_results_csv, fieldnames = ['scenario', 'effort'])
writer.writeheader()
# Write the results dictionary to a csv file
for i in range(len(exp1_scenarios)):
	writer.writerow({'scenario':exp1_scenarios[i],
					 'effort':exp1_effort_values[i]})
# Close the csv file
exp1_results_csv.close()

# Write scenario results (effort values for Blue agent) from scenarios in 
# experiment 2 to a CSV file
exp2_results_csv = open('../../data/model/experimentb.csv','w')
keys = exp2_scenarios
writer = csv.DictWriter(exp2_results_csv, fieldnames = ['scenario', 'effort'])
writer.writeheader()
# Write the results dictionary to a csv file
for i in range(len(exp2_scenarios)):
	writer.writerow({'scenario':exp2_scenarios[i],
					 'effort':exp2_effort_values[i]})
# Close the csv file
exp2_results_csv.close()