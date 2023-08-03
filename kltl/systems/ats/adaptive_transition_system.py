"""
test_transition_system.py
Description:
    A transition system for the robot motion planning example.
"""

from typing import List, Set, Tuple

from kltl.types import Action, AtomicProposition
from .ats_types import ATSState, ATSTransition
from kltl.automata import DeterministicRabinAutomaton
from .. import TransitionSystem


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

    def product(self, automaton: DeterministicRabinAutomaton):
        """
        product_ts = ts.product(automaton)
        Description:
            Creates the product of the transition system and a NFA.
        :param automaton:
        :return:
        """

        # Input Processing
        assert isinstance(automaton, DeterministicRabinAutomaton), f"Input {automaton} is not a DeterministicRabinAutomaton!"

        # Create the product's states
        S_prime = [(s, q) for s in self.S for q in automaton.Q]

        # Create the product's transition relation
        transitions_prime = []
        for (s, act, t_index) in self.transitions:
            for (q, sigma_index, p) in automaton.transitions:
                if automaton.Sigma[sigma_index] == set(self.L(self.S[t_index])):
                    transitions_prime += [(
                        S_prime.index((self.S[s], automaton.Q[q])),
                        act,
                        S_prime.index((self.S[t_index], automaton.Q[p]))
                    )]

        transitions_prime = list(set(transitions_prime))  # Make sure there aren't duplicates

        # Create the initial states of the product
        I_prime = []
        for s0 in self.I:
            for (q0_index, sigma, q_index) in automaton.transitions:
                if automaton.Q[q0_index] in automaton.Q0 and automaton.Sigma[sigma] == set(self.L(s0)):
                    I_prime += [(s0, automaton.Q[q_index])]

        # Create output system
        ts_out = TransitionSystem(S_prime, self.Act, automaton.Q, I=I_prime, transitions=transitions_prime)

        # Create the labels of the system.
        for (s, q) in S_prime:
            ts_out.add_label((s, q), q)

        return ts_out

