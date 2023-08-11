"""
deterministic_rabin.py
Description:
    A deterministic rabin automaton definition.
"""

from typing import List, Set, Tuple

import numpy as np

from kltl.types import State, Action, AtomicProposition, Transition, TransitionMatrix

class DeterministicRabinAutomaton(object):
    def __init__(
        self,
        Q: List[State],
        Sigma: List[Set[AtomicProposition]],
        Q0: List[State] = None,
        transitions: TransitionMatrix = None,
        F: List[Tuple[Set[State],Set[State]]] = None,
    ):
        # Input Processing
        assert len(Q) > 0

        if Q0 is None:
            Q0 = []
        if transitions is None:
            transitions = np.zeros((0, 3), dtype=int)
        if F is None:
            F = []

        self.Q = Q
        self.Sigma = Sigma
        self.Q0 = Q0
        self.transitions = transitions
        self.F = F

    def add_transition(self, q1: State, sigma: Set[AtomicProposition], q2: State):
        assert q1 in self.Q, f" State {q1} is not in state space!"
        assert q2 in self.Q, f" State {q2} is not in state space!"
        assert sigma in self.Sigma

        if self.transition_exists(q1, sigma, q2):
            return

        self.transitions = np.vstack(
            (self.transitions, np.array([(self.Q.index(q1), self.Sigma.index(sigma), self.Q.index(q2))], dtype=int)),
        )

    def transition_exists(self, q1: State, sigma: Set[AtomicProposition], q2: State) -> bool:
        """
        tf = transition_exists(q1, sigma, q2)
        :param q1:
        :param sigma:
        :param q2:
        :return:
        """
        matching_transition_indices = np.argwhere(
            np.all(
                self.transitions == np.array([self.Q.index(q1), self.Sigma.index(sigma), self.Q.index(q2)]),
                axis=-1,
            )
        )
        return len(matching_transition_indices) > 0

    def post(self, q: State, sigma: Set[AtomicProposition] = None) -> List[State]:
        assert q in self.Q, f"State {s} is not in state space!"
        assert (sigma in self.Sigma) or (sigma is None), f"Action {sigma} is not in action space!"

        if sigma is None:
            transitions_from_q = np.argwhere(
                self.transitions[:, 0] == self.Q.index(q)
            ).flatten()
            matching_transitions = self.transitions[transitions_from_q, :]
            successor_states = matching_transitions[:, 2]
        else:
            transitions_from_q = np.argwhere(
                np.logical_and(
                    self.transitions[:, 0] == self.Q.index(q),
                    self.transitions[:, 1] == self.Sigma.index(sigma),
                )
            ).flatten()
            matching_transitions = self.transitions[transitions_from_q, :]
            successor_states = matching_transitions[:, 2]

        return [self.Q[q] for q in successor_states]

    def add_accepting_pair(self, F_i: Set[State], I_i: Set[State]):
        """
        add_accepting_pair
        Description:
            Adds a pair of accepting sets to the automaton.
        :param F_i:
        :param I_i:
        :return:
        """
        assert set(F_i).issubset(set(self.Q)), f"Accepting set {F_i} is not a subset of the state space!"
        assert set(I_i).issubset(set(self.Q)), f"Accepting set {I_i} is not a subset of the state space!"

        if (set(F_i), set(I_i)) not in self.F:
            self.F += [(set(F_i), set(I_i))]
