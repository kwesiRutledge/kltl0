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
