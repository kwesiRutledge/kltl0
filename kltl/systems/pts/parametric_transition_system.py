"""
ParametricTransitionSystem.py
Description:
    A parametric transition system for the robot motion planning example.
"""

from typing import List, Set, Tuple
import numpy as np

from kltl.types import State, Action, AtomicProposition, Output
from .pts_types import Transition, Parameter

class ParametricTransitionSystem:
    """
    ParametricTransitionSystem
    Description:
        A class representing a parametric transition system.
    """
    def __init__(
            self,
            S: List[State],
            Act: List[Action],
            AP: List[AtomicProposition],
            I: List[State] = None,
            Y: List[Output] = None,
            Theta: List[Parameter] = None,
            transitions: List[Transition] = None,
            labels: List[Tuple[State, AtomicProposition]] = None,
            output_map: List[Tuple[State, Parameter, Output]] = None,
    ):
        # Input Processing
        assert len(S) > 0

        if I is None:
            I = []
        if Y is None:
            Y = []
        if Theta is None:
            Theta = []
        if transitions is None:
            transitions = np.zeros((0, 4), dtype=int)
        if labels is None:
            labels = np.zeros((0, 2), dtype=int)
        if output_map is None:
            output_map = np.zeros((0, 3), dtype=int)

        self.S = S
        self.Act = Act
        self.AP = AP
        self.I = I
        self.transitions = transitions
        self.labels = labels

        if Theta == []:
            Theta = ["theta1"]
        self.Theta = Theta

        if Y == []:  # If Y is undefined, then give it the value of the state set.
            Y = S
        self.Y, self.output_map = Y, output_map

    def add_transition(self, s1: State, a: Action, theta: Parameter, s2: State):
        assert s1 in self.S, f" State {s1} is not in state space!"
        assert s2 in self.S, f" State {s2} is not in state space!"
        assert theta in self.Theta, f"Parameter {theta} is not in parameter space!"
        assert a in self.Act

        if self.transition_exists(s1, a, theta, s2):
            return

        self.transitions = np.vstack(
            (self.transitions, [(self.S.index(s1), self.Act.index(a), self.Theta.index(theta), self.S.index(s2))]),
        )

    def transition_exists(self, s1: State, a: Action, theta: Parameter, s2: State):
        matching_transition_indices = np.argwhere(
            np.all(
                self.transitions == np.array([self.S.index(s1), self.Act.index(a), self.Theta.index(theta), self.S.index(s2)]),
                axis=-1,
            )
        )
        return len(matching_transition_indices) > 0

    def add_label(self, s: State, ap: AtomicProposition):
        assert s in self.S, f" State {s} is not in state space!"
        assert ap in self.AP, f"Proposition {ap} is not in atomic proposition space!"

        if self.label_exists(s, ap):
            return

        self.labels = np.vstack(
            (self.labels, np.array([self.S.index(s), self.AP.index(ap)], dtype=int))
        )

    def label_exists(self, s1: State, ap: AtomicProposition):
        matching_transition_indices = np.argwhere(
            np.all(
                self.labels == np.array([self.S.index(s1), self.AP.index(ap)]),
                axis=-1,
            )
        )
        return len(matching_transition_indices) > 0

    def add_output(self, s: State, theta: Parameter, o: Output):
        """
        add_output
        Description:
            Adds output to the transition system (if it doesn't already exist).
        :param s:
        :param theta:
        :param o:
        :return:
        """
        assert s in self.S, f" State {s} is not in state space!"
        assert theta in self.Theta, f"Parameter {theta} is not in parameter space!"
        assert o in self.Y, f" Output {o} is not in the output space!"

        if self.output_exists(s, theta, o):
            return

        self.output_map = np.vstack(
            (self.output_map, np.array([(self.S.index(s), self.Theta.index(theta), self.Y.index(o))], dtype=int)),
        )

    def output_exists(self, s1: State, theta: Parameter, o: Output):
        matching_transition_indices = np.argwhere(
            np.all(
                self.output_map == np.array([self.S.index(s1), self.Theta.index(theta), self.Y.index(o)]),
                axis=-1,
            )
        )
        return len(matching_transition_indices) > 0

    def post(self, s: State, a: Action = None, theta: Parameter = None) -> List[State]:
        assert s in self.S, f"State {s} is not in state space!"
        assert (a in self.Act) or (a is None), f"Action {a} is not in action space!"
        assert (theta in self.Theta) or (theta is None), f"Parameter {theta} is not in parameter space!"

        successor_states = []
        if (a is None) and (theta is None):
            transitions_from_s = np.argwhere(self.transitions[:, 0] == self.S.index(s)).flatten()
            matching_transitions = self.transitions[transitions_from_s, :]
            successor_states = matching_transitions[:, 3]
        elif a is None:
            transitions_from_s_with_theta = np.argwhere(
                np.logical_and(
                    self.transitions[:, 0] == self.S.index(s),
                    self.transitions[:, 2] == self.Theta.index(theta),
                )
            ).flatten()
            matching_transitions = self.transitions[transitions_from_s_with_theta, :]
            successor_states = matching_transitions[:, 3]
        elif theta is None:
            transitions_from_s_with_a = np.argwhere(
                np.logical_and(
                    self.transitions[:, 0] == self.S.index(s),
                    self.transitions[:, 1] == self.Act.index(a),
                )
            ).flatten()
            matching_transitions = self.transitions[transitions_from_s_with_a, :]
            successor_states = matching_transitions[:, 3]
        else:
            transitions_from_s_with_a_and_theta = np.argwhere(
                np.logical_and(
                    self.transitions[:, 0] == self.S.index(s),
                    np.logical_and(
                        self.transitions[:, 1] == self.Act.index(a),
                        self.transitions[:, 2] == self.Theta.index(theta),
                    )
                )
            ).flatten()
            matching_transitions = self.transitions[transitions_from_s_with_a_and_theta, :]
            successor_states = matching_transitions[:, 3]

        # Collect the successor states
        return [self.S[s2] for s2 in successor_states]

    def L(self, s: State) -> List[AtomicProposition]:
        """
        l = ts.L(s)
        Description:
            Defines te
        :param s:
        :return:
        """
        # Input Processing
        assert s in self.S, f" State {s} is not in state space!"

        # Return
        labels_for_s = np.argwhere(self.labels[:, 0] == self.S.index(s)).flatten()
        matching_labels = self.labels[labels_for_s, 1]
        return [self.AP[ap1] for ap1 in matching_labels]

    def O(self, s: State, theta: Parameter = None) -> List[Output]:
        """
        O_s = ts.O(s)
        Description
            Defines the outputs associated with the state s.
        :param s: The state at which we evaluate the outputs.
        :return O_s: The set of outputs possible for state s.
        """

        # Input Processing
        assert s in self.S, f" State {s} is not in state space!"

        # Return
        output_list = []
        if theta is None:
            outputs_from_s = np.argwhere(
                self.output_map[:, 0] == self.S.index(s)
            ).flatten()
            output_list = self.output_map[outputs_from_s, 2]
        else:
            assert theta in self.Theta, f"Parameter {theta} is not in parameter space!"
            outputs_from_s_with_theta = np.argwhere(
                np.logical_and(self.output_map[:, 0] == self.S.index(s), self.output_map[:, 1] == self.Theta.index(theta))
            ).flatten()
            output_list = self.output_map[outputs_from_s_with_theta, 2]

        # Get unique elements of O_s
        O_s = [self.Y[o1] for o1 in output_list]
        return list(set(O_s))

