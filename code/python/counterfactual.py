import moral_kinematics_scenarios as scenarios
import pymunk
from pymunk.vec2d import Vec2d
import pygame
import pymunk.pygame_util
from pygame.locals import *
import handlers
from agents import Agent
from math import sin, cos, radians

def counterfactual_simulation(environment,std_dev,num_times,view=False):
    # Determine counterfactual probability
    #   collision
    counterfactual_prob = 0.0
    true_env = environment(view)
    true_env.run()
    true_outcome = true_env.patient_fireball_collision
    for _ in range(num_times):
        env = environment(view)
        env.agent_patient_collision = true_env.agent_patient_collision
        env.agent_fireball_collision = true_env.agent_fireball_collision
        # Run the counterfactual simulation
        env.counterfactual_run(std_dev)
        # Determine outcome
        counterfactual_outcome = env.patient_fireball_collision
        counterfactual_prob += int(true_outcome == counterfactual_outcome)
    return counterfactual_prob / num_times

def iterate_std_dev(environment,start,end,step,num_times):
    # Retrieve true oucome of simulation w/o noise
    std_dev_prob_map = {}
    for std_dev in range(start,end,step):
        counterfactual_prob = counterfactual_simulation(environment,
                                                        std_dev,num_times)
        std_dev_prob_map[std_dev] = counterfactual_prob
    return std_dev_prob_map

def run():
    for scene in scenarios.__experiment3__:
        sim = getattr(scenarios, scene)
        true_env = sim(True)
        true_env.run()
        env = sim(True)
        env.agent_patient_collision = true_env.agent_patient_collision
        env.agent_fireball_collision = true_env.agent_fireball_collision
        env.counterfactual_run(1, "counter_1"+scene)

def run_rotate():

    def rotate(obj,theta=-20,origin=(500,300)):
        '''
        Rotates objects about a center
        '''
        # Translate w/r to visual origin (500,300)
        obj.body.position -= Vec2d(origin)
        # Radians to degrees
        theta = radians(theta)
        x, y = obj.body.position
        x_ = x*cos(theta) - y*sin(theta)
        y_ = y*cos(theta) + x*sin(theta)
        obj.body.position = [x_,y_]
        # Translate w/r to actual origin (0,0)
        obj.body.position += Vec2d(origin)

    for scene in [scenarios.__experiment3__[14]]:
        sim = getattr(scenarios, scene)
        env = sim(True)
        env.run()
        # Gather position data
        pos = env.position_dict
        agent_positions = env.position_dict['agent']
        patient_positions = env.position_dict['patient']
        fireball_positions = env.position_dict['fireball']

        # Setup pygame and pymunk
        space = pymunk.Space()
        space.damping = 0.05
        screen = pygame.display.set_mode((1000,600))
        options = pymunk.pygame_util.DrawOptions(screen)
        clock = pygame.time.Clock()
        # Setup empty agents
        agent = Agent(0,0,'blue',0,[])
        patient = Agent(0,0,'green',0,[])
        fireball = Agent(0,0,'red',0,[])
        # Add agent to space
        space.add(agent.body, agent.shape,
                  patient.body, patient.shape,
                  fireball.body, fireball.shape)
        pygame.init()
        running = True

        while running:
            # if not handlers.AP_COLLISION: self.agent_patient_collision = self.tick
            try:
                # Extract position data
                a_pos = agent_positions.pop(0)
                p_pos = patient_positions.pop(0)
                f_pos = fireball_positions.pop(0)
                # Set positions of objects
                agent.body.position = Vec2d(a_pos['x'],a_pos['y'])
                patient.body.position = Vec2d(p_pos['x'],p_pos['y'])
                fireball.body.position = Vec2d(f_pos['x'],f_pos['y'])
                # Rotate objects about the center
                rotate(agent)
                rotate(patient)
                rotate(fireball)
                # Render space on screen (if requested)
                screen.fill((255,255,255))
                space.debug_draw(options)
                pygame.display.flip()
                clock.tick(60)
                space.step(1/60.0)
            except Exception as e:
                running = False
run()
