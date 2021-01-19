import moral_kinematics_scenarios as scenarios
import pymunk
from pymunk.vec2d import Vec2d
import pygame
import pymunk.pygame_util
from pygame.locals import *
import handlers
from agents import Agent
from math import sin, cos, radians

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

def run():
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


def run_rotate():

    def rotate(obj,theta=20,origin=(500,300)):
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

    for scene in [scenarios.__experiment3__[0]]:
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
run_rotate()
