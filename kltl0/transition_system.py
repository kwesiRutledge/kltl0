"""
test_transition_system.py
Description:
    A transition system for the robot motion planning example.
"""

from typing import List, Set, Tuple

from kltl0.types import State, Action, AtomicProposition, Transition

class TransitionSystem():
    S: List[State] = []
    I: List[State] = []
    Act: List[Action] = []
    transitions: List[Transition] = None
    AP: List[AtomicProposition] = []
    labels: List[Tuple[State, AtomicProposition]] = None

    def __init__(
            self,
            S: List[State], Act: List[Action], AP: List[AtomicProposition],
            I: List[State] = None, transitions: List[Transition] = None, labels: List[Tuple[State, AtomicProposition]] = None,
    ):
        # Input Processing
        assert len(S) > 0

        self.S = S
        self.Act = Act
        self.AP = AP
        if I is None:
            self.I = [S[0]]
        else:
            self.I = I

        if transitions is None:
            self.transitions = []
        else:
            self.transitions = transitions

        if self.labels is None:
            self.labels = []
        else:
            self.labels = labels

    def add_transition(self, s1: State, a: Action, s2: State):
        assert s1 in self.S
        assert s2 in self.S
        assert a in self.Act

        self.transitions += [(self.S.index(s1), self.Act.index(a), self.S.index(s2))]

    def add_label(self, s: str, a: str):
        assert s in self.S
        assert a in self.Act

        self.labels += [(self.S.index(s), self.Act.index(a))]

    def post(self, s: State, a: Action=None) -> List[str]:
        assert s in self.S
        assert a in self.Act

        if a is None:
            return {s2 for (s1, a1, s2) in self.transitions if s1 == s}
        else:
            return {s2 for (s1, a1, s2) in self.transitions if s1 == s and a in self.Act}