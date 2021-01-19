import pymunk
from pymunk.vec2d import Vec2d
import pygame
import pymunk.pygame_util
from pygame.locals import *
import handlers
from agents import Agent
from math import sin, cos, radians

def rotate(agent,theta):
    theta = radians(theta)
    x = agent.body.position[0]
    y = agent.body.position[1]
    x_ = x*cos(theta) - y*sin(theta)
    y_ = y*cos(theta) + x*sin(theta)
    agent.body.position = [x_,y_]

# Setup pygame and pymunk
space = pymunk.Space()
space.damping = 0.05
screen = pygame.display.set_mode((1000,600))
options = pymunk.pygame_util.DrawOptions(screen)
clock = pygame.time.Clock()

x = 100
y = 300
color = "blue"
collision = 0
moves = []

agent = Agent(x,y,color,collision,moves)

# Add agent to space
space.add(agent.body, agent.shape)

velocity = 300
trajectory = [Vec2d(300,300),Vec2d(800,300)]
a_generator = agent.vec_move(trajectory,velocity,clock,screen,space,options,True,0)
pygame.init()

running = True
while running:
    # if not handlers.AP_COLLISION: self.agent_patient_collision = self.tick
    try:
        # Generate the next tick in the simulation for each object
        next(a_generator)
        # Render space on screen (if requested)
        screen.fill((255,255,255))
        space.debug_draw(options)
        pygame.display.flip()
        clock.tick(60)
        space.step(1/60.0)
    except Exception as e:
        print(e)
        running = False
print(agent.position_dict)
print("Effort expended: ", agent.effort_expended)
pygame.quit()
pygame.display.quit()
