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

moral_kinematics_scenarios = [push_patient]

# Create list of lists of scenarios
list_of_scenarios = [moral_kinematics_scenarios]

# Names of lists
names = ['mk']

# Path to save JSON data to
path = '../../data/json/'

def convert(environment, path=""):
	# Init environment
	env = environment(view=False)

	# Set up config for json file
	sim_dict = {} # Dict to be converted to json
	config = {'scene' : env.screen_size[0]} # Screen size (y-axis)
	config['name'] = environment.__name__ # Name of scenario

	# Init dictionaries for body positions
	bodies_dict = {}

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

for scenarios in list_of_scenarios:
	scenario_type = names[0]
	for scene in scenarios:
		convert(scene, path)