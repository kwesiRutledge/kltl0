"""
trajectory.py
Description:
    A module for managing trajectories of a transition system.
"""

from typing import List, Tuple, Union, Dict
import numpy as np

from kltl.systems.ts import FiniteTrace, InfiniteTrace
from kltl.types import State, Action, AtomicProposition, Transition
from kltl.systems.ts import TransitionSystem

class FiniteTrajectory:
    def __init__(self, trajectory_string: List[Union[State, Action]], system: TransitionSystem):
        # Input Processing
        assert len(trajectory_string) > 0
        assert len(trajectory_string) % 2 == 1, f"Trajectory should have an odd number of entries, but found {len(trajectory_string)}!"

        # Parse the trajectory into state and action parts
        self.states, self.actions = decompose_string_into_states_and_actions(trajectory_string, system)

        self.system = system

    def s(self, state_idx: int):
        assert (state_idx >= 0) and (state_idx < len(self.states)), f"There are only {len(self.states)} states, but user tried to access {state_idx} state!"
        return self.states[state_idx]

    def a(self, action_idx: int):
        """
        Collects action
        :param action_idx:
        :return:
        """
        assert (action_idx >= 0) and (action_idx < len(self.actions)), \
            f"There are only {len(self.actions)} actions, but user tried to access {action_idx} action!"
        return self.actions[action_idx]

    def __len__(self):
        return len(self.states)

    def trace(self):
        trace_as_list = [self.system.L(s) for s in self.states]
        return FiniteTrace(trace_as_list, self.system)

class InfiniteTrajectory:
    """
    Description:
        The infinite trajectory is formed with a prefix that is followed by an infinitely repeating suffix.
    """
    def __init__(self, prefix: List[Union[State, Action]], suffix: List[Union[State, Action]], system: TransitionSystem):
        # Input Processing
        assert (len(prefix) > 0) or (len(suffix) > 0), f"prefix and suffix were both zero length. One of them should be non-empty."
        assert len(prefix) + len(suffix) % 2 == 1, \
            f"Prefix should have an even number of entries, but found {len(suffix) + len(prefix)}!"

        # Parse the trajectory into state and action parts
        self.prefix_states, self.prefix_actions = decompose_string_into_states_and_actions(prefix, system)
        self.suffix_states, self.suffix_actions = decompose_string_into_states_and_actions(suffix, system)

        self.system = system

    def s(self, state_index: int):
        """
        s
        Description:
            Finds the state
        :param state_index:
        :return:
        """
        assert state_index >= 0, f"state index must be nonnegative; received {state_index}"

        # Check if the state is part of the finite prefix
        if state_index < len(self.prefix_states):
            return self.prefix_states[state_index]
        else:
            suffix_index = state_index - len(self.prefix_states)  # Should treat the index as if it "starts" at suffix
            suffix_index = suffix_index % len(self.suffix_states)  # The suffix is infinitely repeating.
            return self.suffix_states[state_index]

    def a(self, action_index: int):
        """
        act_i = a(idx)
        Description:
            Finds the action at the target index.
        :param action_index:
        :return:
        """
        assert action_index >= 0, f"state index must be nonnegative; received {action_index}"

        # Check if the state is part of the finite prefix
        if action_index < len(self.prefix_actions):
            return self.prefix_actions[action_index]
        else:
            suffix_index = action_index - len(
                self.prefix_actions)  # Should treat the index as if it "starts" at suffix
            suffix_index = suffix_index % len(self.suffix_actions)  # The suffix is infinitely repeating.
            return self.suffix_states[action_index]

    def __len__(self):
        return np.inf

    def trace(self):
        trace_prefix_as_list = [self.system.L(s) for s in self.prefix_states]
        trace_suffix_as_list = [self.system.L(s) for s in self.suffix_states]
        return InfiniteTrace(trace_prefix_as_list, trace_suffix_as_list, self.system)

def decompose_string_into_states_and_actions(trajectory_as_string: str, system: TransitionSystem)->Tuple[List[State],List[Action]]:
    """
    decompose_string_into_states_and_actions
    Description:
    :param trajectory_as_string:
    :return:
    """
    # Constants
    state_sequence, action_sequence = [], []
    for (traj_i, elt) in enumerate(trajectory_as_string):
        if traj_i % 2 == 0:  # Every even entry should be a state
            assert elt in system.S, f"State {elt} is not in state space!"
            state_sequence += [elt]
        else:  # Every odd entry should be an action
            assert elt in system.Act, f"Action {elt} is not in action space!"
            action_sequence += [elt]

    return state_sequence, action_sequence

def create_random_trajectory_with_N_actions(sys: TransitionSystem, N: int):
    """
    finite_traj = create_random_trajectory_with_N_actions(sys, N)
    :param sys:
    :param N:
    :return:
    """

    # Select an initial condition
    I_indices = [sys.S.index(s) for s in sys.I]
    s0_index = np.random.choice(I_indices, 1)
    s0 = sys.S[s0_index]

    s_i = s0
    trajectory_as_list = [s0]
    for step_idx in range(N):
        post_si = []
        while len(post_si) == 0:  # Keep sampling actions until post is non empty
            a_i = np.random.choice(sys.Act, 1)[0]
            post_si = sys.post(s_i, a_i)

        s_ip1 = np.random.choice(post_si, 1)[0]

        # Append
        trajectory_as_list += [a_i, s_ip1]

        # Update
        s_i = s_ip1

    return FiniteTrajectory(trajectory_as_list, sys)

def create_closed_loop_trajectory_with_N_steps(
    sys: TransitionSystem,
    N: int,
    policy: Dict[State, Action],
):
    """
    finite_traj = create_closed_loop_trajectory_with_N_steps(sys, N, policy)
    Description:
        Creates a closed loop trajectory with N steps.
    :param sys:
    :param N:
    :param policy: A dictionary that maps the current state to an action.
        TODO: Create a more universal way for defining policies
    :return:
    """

    # Select an initial condition
    I_indices = [sys.S.index(s) for s in sys.I]
    s0 = np.random.choice(I_indices, 1)[0] # Index of first state

    # Simulate
    s_i = s0
    trajectory_as_list = [sys.S[s0]]
    for step_idx in range(N):
        post_si = []
        while len(post_si) == 0:  # Keep sampling actions until post is non empty
            a_i = policy[s_i][0]
            post_si = sys.post_indices(sys.S[s_i], a_i)

        s_ip1 = np.random.choice(post_si, 1)[0]

        # Append
        trajectory_as_list += [a_i, sys.S[s_ip1]]

        # Update
        s_i = s_ip1

    return FiniteTrajectory(trajectory_as_list, sys)