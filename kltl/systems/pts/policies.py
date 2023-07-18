"""
policies.py
Description:
    A module for the finding the possible trajectories given the control policies of a parametric transition system.
"""

from typing import List, Tuple
import numpy as np
from kltl.systems.pts.trajectory import create_random_trajectory_with_N_actions
from kltl.systems.pts.sadra import get_sadra_system
from kltl.systems.pts.parametric_transition_system import ParametricTransitionSystem

class ControlPolicies:
    def __init__(self, test_num=1):
        self.tested = 0
        self.entered = False
        self.test_num = test_num
        
    def find(self, transitions: List[Tuple], dir: str):
        # IDE raises error due to early reference of object 'sadra', but can still run code as this function is only called after object is declared.
        return next(transition for transition in transitions if sadra.Act[transition[1]] == dir)
        
    def control_policy_1(self, trajectory: List[str], theta=-1):
        sadra = get_sadra_system()
        coord = sadra.state_name_to_coordinates
        r_idx, c_idx = coord(trajectory[-1])
        (goal1, _), (goal2, _) = sadra.labels
        goal1, goal2 = coord(sadra.Y[goal1]), coord(sadra.Y[goal2])
        reach1, reach2 = False, False
        transitions = []
        
        for i in range(0, len(trajectory), 3):
            y = trajectory[i]

            if coord(y) == goal1: reach1 = True
            if coord(y) == goal2: reach2 = True
            if reach1 and reach2: return None
        
        for transition in sadra.transitions:
            if sadra.Y[transition[0]] == trajectory[-1]:
                transitions.append(transition)
                
        if not reach1:
            if r_idx != goal1[0]:
                if r_idx > goal1[0]: 
                    transition = self.find(transitions, 'up')
                else:
                    transition = self.find(transitions, 'down')
            else:
                if c_idx > goal1[1]: 
                    transition = self.find(transitions, 'left')
                else:
                    transition = self.find(transitions, 'right')
            return sadra.Act[transition[1]], sadra.Y[transition[-1]], sadra.Y[transition[-1]]
            
        # Calculate buffer distance to get to goal 2. We already know theta = -1, and that the windy region is from 3 to 6.
        elif not reach2:
            push_dist = theta*4

            if r_idx < sadra.windy_region_y_lb and c_idx - goal2[1] < -push_dist:
                transition = self.find(transitions, 'right')
            elif r_idx > goal2[0]:
                transition = self.find(transitions, 'up')
            elif r_idx < goal2[0]:
                transition = self.find(transitions, 'down')
            elif c_idx > goal2[1]:
                transition = self.find(transitions, 'left')
            else:
                transition = self.find(transitions, 'right')
            
            return sadra.Act[transition[1]], sadra.Y[transition[-1]], sadra.Y[transition[-1]]
        
    def control_policy_2(self, trajectory: List[str]):
        return self.control_policy_1(trajectory, theta=-2)
        
    def control_policy_3(self, trajectory: List[str]):
        sadra = get_sadra_system()
        coord = sadra.state_name_to_coordinates
        transitions = []
        
        for transition in sadra.transitions:
            if sadra.Y[transition[0]] == trajectory[-1]:
                transitions.append(transition)
                        
        if self.tested < self.test_num:
            if self.entered:
                transition = self.find(transitions, 'up')
                if coord(sadra.Y[transition[-1]])[0] < sadra.windy_region_y_lb: 
                    self.entered = False
                    self.tested += 1
            elif coord(trajectory[-1])[1] < int(sadra.n_cols/2):
                transition = self.find(transitions, 'right')
            elif coord(trajectory[-1])[1] > int(sadra.n_cols/2):
                transition = self.find(transitions, 'left')
            else:
                transition = self.find(transitions, 'down')
                if coord(sadra.Y[transition[-1]])[0] >= sadra.windy_region_y_lb: self.entered = True
            return sadra.Act[transition[1]], sadra.Y[transition[-1]], sadra.Y[transition[-1]]
        else:
            actions = {}
            theta = 0
            
            for i in range(0,len(trajectory)-3, 3):
                if coord(trajectory[i+1])[0] <= sadra.windy_region_y_ub and coord(trajectory[i+1])[0] >= sadra.windy_region_y_lb:
                    transition = trajectory[i+2]
                    if transition not in actions: actions[transition] = coord(trajectory[i+4])[1] - coord(trajectory[i+1])[1]
                    else: actions[transition].append(coord(trajectory[i+4])[1] - coord(trajectory[i+1])[1])
                    
            for action in actions:
                actions[action] = np.array(actions[action])
                
            if 'left' in actions: actions['left'] = actions['left'] + 1
            if 'right' in actions: actions['right'] = actions['right'] - 1
            
            if -2 in actions.values(): theta = -2
            elif 2 in actions.values(): theta = 2 
            elif dict != {} and theta == 0: 
                avg = (np.mean(actions['up']) + np.mean(actions['down']) + np.mean(actions['left']) + np.mean(actions['right']))/4
                if avg > 0: avg = round(avg)
                if avg < 0: avg = -round(-avg)
                theta = avg
                return self.control_policy_1(trajectory, theta=avg)
            
            return self.control_policy_1(trajectory, theta=theta)
        
def get_all_trajectories(policy, max_len: int, pts: ParametricTransitionSystem):
    trajs = [[y0, y0] for y0 in pts.I]
    for i in range(max_len):
        for traj in trajs:
            traj.extend(policy(traj))
    return trajs
        
