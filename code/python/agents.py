'''
Agent Classes for Moral Dynamics.

March 14, 2017
Felix Sosa
'''
import pymunk
import pygame
import glob
# Distance agents move per action
move_lat_distance = 160
move_long_distance = 160
wait_period = 27

class Agent:
	def __init__(self, x, y, color, collision, moves, mass=1, rad=25):
		'''
		Class for agents in scenarios. Used to instantiate the Blue Agent,
		Green Agent, and Fireball in the Moral Dynamics project.

		x 	  -- x dimension of initial location in a scenario
		y	  -- y dimension of initial location in a scenario
		color -- agent's color
		collision -- collision type for agent body (used in pymunk)
		moves -- actions the agent will take for a given scenario
		mass  -- optional mass parameter for agent's body
		rad   -- optional radius for agent's body
		'''
		# Actions available to agents
		self.action_dict = {
			'U':self.move_up,
			'D':self.move_down,
			'R':self.move_right,
			'L':self.move_left,
			'N':self.do_nothing,
			'S':self.stay_put,
			'DS':self.move_down_special,
			'DS2':self.move_down_special_2,
			'RS':self.move_right_special,
			'NS':self.do_nothing_special,
			'NS2':self.do_nothing_special_2
		}
		# Agent attributes
		self.body = pymunk.Body(mass,1)
		self.body.position = (x,y)
		self.shape = pymunk.Circle(self.body, rad)
		self.shape.color = pygame.color.THECOLORS[color]
		self.shape.collision_type = collision
		self.shape.elasticity = 1
		self.effort_expended = 0
		self.actions = [self.action_dict[x] for x in moves]

	# Action definitions
	def move_right(self, velocity, clock, screen, space, options, view):
		# Move agent right
		intended_x_pos = self.body.position[0]+move_lat_distance
		while self.body.position[0] < intended_x_pos:
			if view:
				for event in pygame.event.get():
					pass
			if self.body.velocity[0] < velocity:
				imp = velocity - self.body.velocity[0]
				self.body.apply_impulse_at_local_point((imp,0))
				self.effort_expended += imp
			yield

	def move_left(self, velocity, clock, screen, space, options, view):
		# Move agent left
		intended_x_pos = self.body.position[0]-move_lat_distance
		while self.body.position[0] > intended_x_pos:
			if view:
				for event in pygame.event.get():
					pass
			if abs(self.body.velocity[0]) < velocity:
				imp = velocity - abs(self.body.velocity[0])
				self.body.apply_impulse_at_local_point((-1*imp,0))
				self.effort_expended += imp
			yield

	def move_up(self, velocity, clock, screen, space, options, view):
		# Move agent up
		intended_y_pos = self.body.position[1]+move_long_distance
		while self.body.position[1] < intended_y_pos:
			if view:
				for event in pygame.event.get():
					pass
			if self.body.velocity[1] < velocity:
				imp = velocity - self.body.velocity[1]
				self.body.apply_impulse_at_local_point((0,imp))
				self.effort_expended += imp
			yield

	def move_down(self, velocity, clock, screen, space, options, view):
		# Move agent up
		intended_y_pos = self.body.position[1]-move_long_distance
		while self.body.position[1] > intended_y_pos:
			if view:
				for event in pygame.event.get():
					pass
			if abs(self.body.velocity[1]) < velocity:
				imp = velocity - abs(self.body.velocity[1])
				self.body.apply_impulse_at_local_point((0,-1*imp))
				self.effort_expended += imp
			yield

	def stay_put(self, velocity, clock, screen, space, options, view):
		# Agent stays put. This is different from do_nothing in that the 
		# agent will apply a force to maintain its current location if 
		# pushed or pulled in some direction.
		for _ in range(wait_period):
			if view:
				for event in pygame.event.get():
					pass
			if abs(self.body.velocity[1]) > 0:
				imp = -1*self.body.velocity[1]
				self.body.apply_impulse_at_local_point((0,imp))
				self.effort_expended += abs(imp)
				print(self.effort_expended)
			if abs(self.body.velocity[0]) > 0:
				imp = -1*self.body.velocity[0]
				self.body.apply_impulse_at_local_point((imp,0))
				self.effort_expended += abs(imp)
			yield

	def move_right_special(self,velocity,clock,screen,space,options,view):
		# Move agent right (special case for replicating scenarios in 
		# Moral Kinematics)
		tick = 0
		intended_x_pos = self.body.position[0]+move_lat_distance+move_lat_distance*0.6
		while self.body.position[0] < intended_x_pos:
			if view:
				for event in pygame.event.get():
					pass
			tick += 1
			if self.body.velocity[0] < velocity:
				imp = velocity - self.body.velocity[0]
				self.body.apply_impulse_at_local_point((imp,0))
				self.effort_expended += abs(imp)
			yield

	def move_down_special(self,velocity,clock,screen,space,options,view,t=None,n=None):
		# Move agent down (special case for replicating scenarios in 
		# Moral Kinematics)
		intended_y_pos = self.body.position[1]-move_long_distance/3.0
		while self.body.position[1] > intended_y_pos:
			if view:
				for event in pygame.event.get():
					pass
			if abs(self.body.velocity[1]) < velocity:
				imp = velocity - abs(self.body.velocity[1])
				self.body.apply_impulse_at_local_point((0,-1*imp))
				self.effort_expended += abs(imp)
			yield
		for _ in range(2*wait_period/3):
			if view:
				for event in pygame.event.get():
					pass
			yield

	def move_down_special_2(self,velocity,clock,screen,space,options,view,t=None,n=None):
		# Move agent down (special case for replicating scenarios in 
		# Moral Kinematics)
		intended_y_pos = self.body.position[1]-move_long_distance/2.5
		while self.body.position[1] > intended_y_pos:
			if view:
				for event in pygame.event.get():
					pass
			if abs(self.body.velocity[1]) < velocity:
				imp = velocity - abs(self.body.velocity[1])
				self.body.apply_impulse_at_local_point((0,-1*imp))
				self.effort_expended += abs(imp)
			yield
		for _ in range(wait_period/2):
			if view:
				for event in pygame.event.get():
					pass
			yield
	
	def do_nothing(self,velocity,clock,screen,space,options,view,t=None,n=None):
		# Agent does nothing
		for _ in range(wait_period):
			if view:
				for event in pygame.event.get():
					pass
			yield

	def do_nothing_special(self,velocity,clock,screen,space,options,view,t=None,n=None):
		# Do nothing (special case for replicating scenarios in 
		# Moral Kinematics)
		for _ in range(wait_period+5):
			if view:
				for event in pygame.event.get():
					pass
			yield

	def do_nothing_special_2(self,velocity,clock,screen,space,options,view,t=None,n=None):
		# Do nothing (special case for replicating scenarios in 
		# Moral Kinematics)
		for _ in range(wait_period+10):
			if view:
				for event in pygame.event.get():
					pass
			yield

	def act(self, velocity, clock, screen, space, options, view):
		# Execute policy
		actions = iter(self.actions)
		actions_left = True
		action = next(actions)
		while actions_left:
			try:
				for _ in action(velocity, clock, screen, space, options, view):
					yield
				action = next(actions)
			except:
				return