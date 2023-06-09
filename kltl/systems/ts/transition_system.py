"""
test_transition_system.py
Description:
    A transition system for the robot motion planning example.
"""

from typing import List, Set, Tuple

from kltl.types import State, Action, AtomicProposition, Transition

class TransitionSystem():
    S: List[State] = []
    I: List[State] = []
    Act: List[Action] = []
    transitions: List[Transition] = []
    AP: List[AtomicProposition] = []
    labels: List[Tuple[State, AtomicProposition]] = []

    def __init__(
            self,
            S: List[State], Act: List[Action], AP: List[AtomicProposition],
            I: List[State] = [],
            transitions: List[Transition] = [], labels: List[Tuple[State, AtomicProposition]] = [],
    ):
        # Input Processing
        assert len(S) > 0

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

        self.transitions += [(self.S.index(s1), self.Act.index(a), self.S.index(s2))]

    def add_label(self, s: State, ap: AtomicProposition):
        assert s in self.S, f" State {s} is not in state space!"
        assert ap in self.AP, f"Proposition {ap} is not in atomic proposition space!"

        self.labels += [(self.S.index(s), self.AP.index(ap))]

    def post(self, s: State, a: Action = None) -> List[State]:
        assert s in self.S, f"State {s} is not in state space!"
        assert (a in self.Act) or (a is None), f"Action {a} is not in action space!"

        if a is None:
            return [self.S[s2] for (s1, a1, s2) in self.transitions if s1 == self.S.index(s)]
        else:
            return [self.S[s2] for (s1, a1, s2) in self.transitions if s1 == self.S.index(s) and a1 == self.Act.index(a)]

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
        return [self.AP[ap1] for (s1, ap1) in self.labels if s1 == self.S.index(s)]
