"""
test_transition_system.py
Description:
    A transition system for the robot motion planning example.
"""

from typing import List, Set, Tuple
import networkx as nx
import numpy as np

from kltl.systems.graph_utils import transition_matrix2adjacency_matrix
from kltl.types import State, Action, AtomicProposition, Transition

class TransitionSystem(object):
    def __init__(
            self,
            S: List[State], Act: List[Action], AP: List[AtomicProposition],
            I: List[State] = None,
            transitions: np.array = None,
            labels: np.array = None,
    ):
        # Input Processing
        assert len(S) > 0

        if I is None:
            I = []
        if transitions is None:
            transitions = np.zeros((0, 3), dtype=int)
        if labels is None:
            labels = np.zeros((0, 2), dtype=int)

        self.S = S
        self.Act = Act
        self.AP = AP
        self.I = I
        self.transitions = transitions
        self.labels = labels

    def add_transition(self, s1: State, a: Action, s2: State):
        assert s1 in self.S, f" State {s1} is not in state space!"
        assert s2 in self.S, f" State {s2} is not in state space!"
        assert a in self.Act

        self.transitions = np.vstack(
            (self.transitions, np.array([self.S.index(s1), self.Act.index(a), self.S.index(s2)], dtype=int))
        )

    def add_label(self, s: State, ap: AtomicProposition):
        assert s in self.S, f" State {s} is not in state space!"
        assert ap in self.AP, f"Proposition {ap} is not in atomic proposition space!"

        self.labels = np.vstack(
            (self.labels, np.array([self.S.index(s), self.AP.index(ap)], dtype=int))
        )

    def post(self, s: State, a: Action = None) -> List[State]:
        assert s in self.S, f"State {s} is not in state space!"
        assert (a in self.Act) or (a is None), f"Action {a} is not in action space!"

        successor_states = []
        if a is None:
            transitions_from_s = np.argwhere(self.transitions[:, 0] == self.S.index(s)).flatten()
            successor_states = self.transitions[transitions_from_s, 2]
        else:
            transitions_from_s_with_a = np.argwhere(
                np.logical_and((self.transitions[:, 0] == self.S.index(s)), (self.transitions[:, 1] == self.Act.index(a)))
            ).flatten()
            successor_states = self.transitions[transitions_from_s_with_a, 2]

        return [self.S[s] for s in successor_states]

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

    def reachable_states_from(self, S_in: List[State]) -> List[State]:
        """
        S_reachable = ts.reachable_states(S_in)
        :param S_in: Set of state to begin from during reachable set computation.
        :return:
        """
        # Constants

        # Start algorithm
        seen_k = set()
        seen_kp1 = set(S_in)

        while seen_k != seen_kp1:
            seen_k = seen_kp1.copy()
            for s in seen_k:
                seen_kp1.update(self.post(s))

        return list(seen_kp1)

    def to_networkx_graph(self):
        """
        G = ts.to_networkx_graph()
        Description:
            Converts the transition system to a networkx graph.
        :return:
        """

        transition_matrix = self.transitions[:, [0, 2]]
        G = nx.DiGraph(
            transition_matrix2adjacency_matrix(self),
        )

        # Add all nodes
        #G.add_nodes_from(range(len(self.S)))
        # G.add_nodes_from([
        #     (s, {'label': self.L(s)}) for s in self.S
        # ])

        # Add all transitions
        # G.add_edges_from([
        #     (self.S[s1], self.S[s2], {'action': self.Act[a]}) for (s1, a, s2) in self.transitions
        # ])

        return G