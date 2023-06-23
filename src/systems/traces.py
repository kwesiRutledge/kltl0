"""
traces.py
Description:
    A module for traces.
"""

from typing import List, Tuple, Union

from src.types import State, Action, AtomicProposition, Transition
from src.systems import TransitionSystem

class Trajectory:
    def __init__(self, trajectory_string: List[Union[State, Action]], system: TransitionSystem):
        # Input Processing
        assert len(trajectory_string) > 0
        assert len(trajectory_string) % 2 == 1, f"Trajectory should have an odd number of entries, but found {len(trajectory_string)}!"

        # Parse the trajectory into state and action parts
        self.s, self.a = [], []
        for (traj_i, elt) in enumerate(trajectory_string):
            if traj_i % 2 == 0: # Every even entry should be a state
                assert elt in system.S, f"State {elt} is not in state space!"
                self.s += [elt]
            else: # Every odd entry should be an action
                assert elt in system.Act, f"Action {elt} is not in action space!"
                self.a += [elt]

