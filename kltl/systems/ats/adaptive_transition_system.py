"""
test_transition_system.py
Description:
    A transition system for the robot motion planning example.
"""

from typing import List, Set, Tuple

from kltl.types import Action, AtomicProposition
from .ats_types import ATSState, ATSTransition

class AdaptiveTransitionSystem(object):
    def __init__(
            self,
            S: List[ATSState], Act: List[Action], AP: List[AtomicProposition],
            I: List[ATSState] = None,
            transitions: List[ATSTransition] = None,
            labels: List[Tuple[ATSState, AtomicProposition]] = None,
    ):
        # Input Processing
        assert len(S) > 0

        if I is None:
            I = []
        if transitions is None:
            transitions = []
        if labels is None:
            labels = []

        self.S = S
        self.Act = Act
        self.AP = AP
        self.I = I
        self.transitions = transitions
        self.labels = labels

    def add_transition(self, s1: ATSState, a: Action, s2: ATSState):
        assert s1 in self.S, f" ATSState {s1} is not in state space!"
        assert s2 in self.S, f" ATSState {s2} is not in state space!"
        assert a in self.Act

        self.transitions += [(self.S.index(s1), self.Act.index(a), self.S.index(s2))]

    def add_label(self, s: ATSState, ap: AtomicProposition):
        assert s in self.S, f" ATSState {s} is not in state space!"
        assert ap in self.AP, f"Proposition {ap} is not in atomic proposition space!"

        print("self.S.index(s)", self.S.index(s))
        print("self.AP.index(ap)", self.AP.index(ap))
        print(self.labels)
        self.labels += [(self.S.index(s), self.AP.index(ap))]

    def post(self, s: ATSState, a: Action = None) -> List[ATSState]:
        assert s in self.S, f"ATSState {s} is not in state space!"
        assert (a in self.Act) or (a is None), f"Action {a} is not in action space!"

        if a is None:
            return [self.S[s2] for (s1, a1, s2) in self.transitions if s1 == self.S.index(s)]
        else:
            return [self.S[s2] for (s1, a1, s2) in self.transitions if s1 == self.S.index(s) and a1 == self.Act.index(a)]

    def L(self, s: ATSState) -> List[AtomicProposition]:
        """
        l = ts.L(s)
        Description:
            Defines te
        :param s:
        :return:
        """
        # Input Processing
        assert s in self.S, f" ATSState {s} is not in state space!"

        # Return
        return [self.AP[ap1] for (s1, ap1) in self.labels if s1 == self.S.index(s)]
