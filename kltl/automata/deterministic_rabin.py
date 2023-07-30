"""
deterministic_rabin.py
Description:
    A deterministic rabin automaton definition.
"""

from typing import List, Set, Tuple

from kltl.types import State, Action, AtomicProposition, Transition

class DeterministicRabinAutomaton(object):
    def __init__(
        self,
        Q: List[State],
        Sigma: List[Set[AtomicProposition]],
        Q0: List[State] = None,
        transitions: List[Transition] = None,
        F: List[Tuple[Set[State],Set[State]]] = None,
    ):
        # Input Processing
        assert len(Q) > 0

        if Q0 is None:
            Q0 = []
        if transitions is None:
            transitions = []
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

        self.transitions += [(self.Q.index(q1), self.Sigma.index(sigma), self.Q.index(q2))]

    def post(self, q: State, sigma: Set[AtomicProposition] = None) -> List[State]:
        assert q in self.Q, f"State {s} is not in state space!"
        assert (sigma in self.Sigma) or (sigma is None), f"Action {sigma} is not in action space!"

        if sigma is None:
            return [self.Q[q2] for (q1, a1, q2) in self.transitions if q1 == self.Q.index(q)]
        else:
            return [self.Q[q2] for (q1, a1, q2) in self.transitions if q1 == self.Q.index(q) and a1 == self.Sigma.index(sigma)]

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
