"""
trajectory.py
Description:
    A module for managing trajectories of a transition system.
"""

from typing import List, Tuple, Union
import numpy as np

from kltl.systems.ts.traces import FiniteTrace, InfiniteTrace
from kltl.types import State, Action, AtomicProposition, Transition, Output
from kltl.systems.pts.pts_types import Parameter
from kltl.systems.pts import ParametricTransitionSystem

class FiniteTrajectory:
    def __init__(
            self,
            trajectory_string: List[Union[State, Action]],
            theta: Parameter,
            system: ParametricTransitionSystem):
        # Input Processing
        assert len(trajectory_string) > 0
        assert len(trajectory_string) % 3 == 2, f"Trajectory should have 3n+2 entries, but found {len(trajectory_string)}!"

        # Parse the trajectory into state and action parts
        self.states, self.actions, self.outputs = decompose_string_into_states_actions_and_outputs(trajectory_string, system)
        self.param = theta

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

    def y(self, output_idx: int) -> Output:
        """
        y_i = ts.y(i)
        :param output_idx: Index in the trajectory where output was measured.
        :return: The value of the output at index i on trajectory.
        """
        assert (output_idx >= 0) and (output_idx < len(self.outputs)), \
            f"There are only {len(self.outputs)} outputs, but user tried to access {output_idx} output!"
        return self.outputs[output_idx]

    def __len__(self):
        return len(self.states)

    def trace(self):
        trace_as_list = [self.system.L(s) for s in self.states]
        return FiniteTrace(trace_as_list, self.system)

    def __str__(self):
        traj_as_str = ""
        for k in range(len(self)-1):
            traj_as_str += self.s(k) + " , "
            traj_as_str += self.y(k) + " , "
            traj_as_str += self.a(k) + " , "
        traj_as_str += self.s(len(self)-1) + " , " + self.y(len(self)-1)
        return traj_as_str


class InfiniteTrajectory:
    """
    Description:
        The infinite trajectory is formed with a prefix that is followed by an infinitely repeating suffix.
    """
    def __init__(self, prefix: List[Union[State, Action]], suffix: List[Union[State, Action]], theta: Parameter, system: ParametricTransitionSystem):
        # Input Processing
        assert (len(prefix) > 0) or (len(suffix) > 0), f"prefix and suffix were both zero length. One of them should be non-empty."
        assert len(prefix) + len(suffix) % 3 == 2, \
            f"Prefix should have an even number of entries, but found {len(suffix) + len(prefix)}!"

        # Parse the trajectory into state and action parts
        self.prefix_states, self.prefix_actions = decompose_string_into_states_actions_and_outputs(prefix, system)
        self.suffix_states, self.suffix_actions = decompose_suffix_into_states_actions_and_outputs(suffix, system)
        self.parameter = theta

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

    def y(self, output_index: int) -> Output:
        """
        y_i = ts.y(i)
        Description:

        :param output_index: (int) Index in the trajectory where output was measured.
        :type output_index: int
        :return: The value of the output at index i on trajectory.
        """
        assert output_index >= 0, f"state index must be nonnegative; received {output_index}"

        # Check if the state is part of the finite prefix
        if output_index < len(self.prefix_outputs):
            return self.prefix_outputs[output_index]
        else:
            suffix_index = output_index - len(self.prefix_outputs)  # Should treat the index as if it "starts" at suffix
            suffix_index = suffix_index % len(self.suffix_outputs)  # The suffix is infinitely repeating.
            return self.suffix_outputs[suffix_index]

    def __len__(self):
        return np.inf

    def trace(self):
        trace_prefix_as_list = [self.system.L(s) for s in self.prefix_states]
        trace_suffix_as_list = [self.system.L(s) for s in self.suffix_states]
        return InfiniteTrace(trace_prefix_as_list, trace_suffix_as_list, self.system)


def decompose_string_into_states_actions_and_outputs(
        trajectory_as_string: str,
        system: ParametricTransitionSystem,
) -> Tuple[List[State], List[Action], List[Output]]:
    """
    decompose_string_into_states_and_actions
    Description:
    :param trajectory_as_string: List of strings that corresponds to the sequence of actions, states and outputs
    :return:
    """
    # Constants
    state_sequence, action_sequence, output_sequence = [], [], []
    for (traj_i, elt) in enumerate(trajectory_as_string):
        if traj_i % 3 == 0:  # Every first entry (out of three) should be a state
            assert elt in system.S, f"State {elt} is not in state space!"
            state_sequence += [elt]
        elif traj_i % 3 == 1: # Every second entry (out of three) should be an output
            assert elt in system.Y, f"Output {elt} is not in output space!"
            output_sequence += [elt]
        else:
            # traj_i % 3 == 2: # Every third entry (out of three) should be an action
            assert elt in system.Act, f"Action {elt} is not in action space!"
            action_sequence += [elt]


    return state_sequence, action_sequence, output_sequence


def decompose_suffix_into_states_actions_and_outputs(
        trajectory_as_string: str,
        system: ParametricTransitionSystem,
) -> Tuple[List[State], List[Action], List[Output]]:
    """
    decompose_string_into_states_and_actions
    Description:
    :param trajectory_as_string: List of strings that corresponds to the sequence of actions, states and outputs
    :return:
    """
    # Constants
    state_sequence, action_sequence, output_sequence = [], [], []
    for (traj_i, elt) in enumerate(trajectory_as_string):
        if traj_i % 3 == 0:
            # traj_i % 3 == 2: # Every third entry (out of three) should be an action
            assert elt in system.Act, f"Action {elt} is not in action space!"
            action_sequence += [elt]
        elif traj_i % 3 == 1:  # Every first entry (out of three) should be a state
            assert elt in system.S, f"State {elt} is not in state space!"
            state_sequence += [elt]
        else:  # Every second entry (out of three) should be an output
            assert elt in system.Y, f"Output {elt} is not in output space!"
            output_sequence += [elt]

    return state_sequence, action_sequence, output_sequence


def create_random_trajectory_with_N_actions(sys: ParametricTransitionSystem, N: int):
    """
    finite_traj = create_random_trajectory_with_N_actions(sys, N)
    :param sys:
    :param N:
    :return:
    """

    # Select an initial condition
    s0 = np.random.choice(sys.I, 1)[0]
    theta = np.random.choice(sys.Theta, 1)[0]
    y0 = np.random.choice(sys.O(s0, theta), 1)[0]

    s_i, y_i = s0, y0
    trajectory_as_list = [s0, y0]
    for step_idx in range(N):
        post_si = []
        assert len(sys.post(s_i, theta=theta)) > 0, f"Post of {s_i} is empty!"
        while len(post_si) == 0:  # Keep sampling actions until post is non empty
            a_i = np.random.choice(sys.Act, 1)[0]
            post_si = sys.post(s_i, a_i, theta)


        s_ip1 = np.random.choice(post_si, 1)[0]
        y_ip1 = np.random.choice(sys.O(s_ip1, theta), 1)[0]

        # Append
        trajectory_as_list += [a_i, s_ip1, y_ip1]

        # Update
        s_i = s_ip1

    return FiniteTrajectory(trajectory_as_list, theta, sys)
