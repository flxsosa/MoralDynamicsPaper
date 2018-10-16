'''
Collision handlers for the pymunk physics engine used for the 
Moral Dynamics project.

April 2, 2017
Felix Sosa
'''
import pygame
import pymunk
from pygame.locals import *

collision = []
PF_COLLISION = []
totalImpulse = []

def rem0(arbiter, space, data):
	'''
	Used with post_solve. Removes the Green Agent after colliding with 
	the Fireball. Expected that Green Agent is in space.shapes[1].
	'''
	if PF_COLLISION:
		return True
	space.remove(space.shapes[1])
	space.remove(space.bodies[1])
	running = False
	PF_COLLISION.append(1)
	pygame.time.set_timer(QUIT, 1000)
	return True