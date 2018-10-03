import json
import sys
import pygame

from moral_kinematics_scenarios import harm_moving_moving,harm_moving_static, \
									harm_static_moving, harm_static_static, \
									victim_moving_moving, victim_moving_static, \
									victim_static_moving, victim_static_static, \
									long_distance, dodge, bystander, stays_put, \
									short_distance, med_push, long_push, \
									push_patient, double_push

# from moral_kinematics_scenarios import long_distance, dodge, bystander, \
# 							  stays_put, short_distance, med_push, long_push, \
# 							  push_patient, double_push

# from counter_scenarios import med_push_fireball, long_push_patient_moving, \
# 							  long_push_fireball_moving, push_against_patient, push_against_fireball, \
# 							  push_patient_oncoming, push_fireball_oncoming, fireball_walks_away, \
# 							  patient_walks_away

# from experiment_4_scenarios_good import good_1, good_2, good_3, good_4, good_5, \
# 							  good_6, good_7, good_8, good_9, good_10, good_11, good_12

# from experiment_4_scenarios_bad import short_distance_fireball, short_distance_patient, \
# 							  push_against_fireball, push_against_patient, bystander_patient, \
# 							  bystander_fireball, long_push_fireball_moving, long_push_patient_moving, \
# 							  stays_put_fireball, stays_put_patient, bump_fireball, bump_patient

# List of scenarios from each of the types
# moral_kinematics_scenarios = [harm_moving_moving,harm_moving_static,
# 								harm_static_moving, harm_static_static,
# 								victim_moving_moving, victim_moving_static,
# 								victim_static_moving, victim_static_static,
# 								long_distance, dodge, bystander, stays_put,
# 								short_distance, med_push, long_push,
# 								push_patient, double_push]

moral_kinematics_scenarios = [push_patient]

# counter_scenarios = [med_push_fireball, long_push_patient_moving, long_push_fireball_moving,
# 							  push_against_patient, push_against_fireball, push_patient_oncoming, 
# 							  push_fireball_oncoming, fireball_walks_away, patient_walks_away]
# experiment_4_scenarios_good =[good_1, good_2, good_3, good_4, good_5, good_6, good_7, 
# 							  good_8, good_9, good_10, good_11, good_12]
# experiment_4_scenarios_bad = [short_distance_fireball, short_distance_patient, push_against_fireball,
# 							  push_against_patient, bystander_patient, bystander_fireball, 
# 							  long_push_fireball_moving, long_push_patient_moving, 
# 							  stays_put_fireball, stays_put_patient, bump_fireball, 
# 							  bump_patient]

# Create list of lists of scenarios
list_of_scenarios = [moral_kinematics_scenarios]
# list_of_scenarios = [moral_kinematics_scenarios, counter_scenarios, 
# 					 experiment_4_scenarios_good, experiment_4_scenarios_bad]
# Names of lists
names = ['mk']#, 'counter', 'exp_4_good', 'exp_4_bad']
path = '../../data/json/'

def convert(environment, path=""):
	# Init environment
	env = environment(view=False,run=False)
	# Set up config for json file
	sim_dict = {} # Dict to be converted to json
	config = {'scene' : env.screen_size[0]} # Screen size (y-axis)
	config['name'] = environment.__name__ # Name of scenario
	# Init dictionaries for body positions
	bodies_dict = {}
	# Run environment
	env.configure()
	env.run()
	# Gather positional data on objects and add to dict
	bodies_dict["agent"] = env.position_dict['agent']
	bodies_dict["patient"] = env.position_dict['patient']
	bodies_dict["fireball"] = env.position_dict['fireball']

	# Convert dict to json
	config['ticks'] = env.tick
	sim_dict['config'] = config
	sim_dict["objects"] = bodies_dict

	# Save json
	with open(path+config['name']+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

i = 0
for scenarios in list_of_scenarios:
	scenario_type = names[i]
	for scene in scenarios:
		convert(scene, path)