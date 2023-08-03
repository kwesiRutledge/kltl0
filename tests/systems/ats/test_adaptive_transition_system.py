"""
test_adaptive_transition_system.py
Description:
    Testing that the adaptive transition system works.
"""
import unittest
from itertools import chain, combinations

from kltl.automata import DeterministicRabinAutomaton
from kltl.systems import AdaptiveTransitionSystem
class TestAdaptiveTransitionSystem(unittest.TestCase):
    def powerset(self, iterable):
        "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
        s = list(iterable)
        return list(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))

    def test_product1(self):
        """
        Description:
            Test that the product of a transition and an automaton is correct.
        :return:
        """
        # Constants


        # Create dummy transition system
        ts1 = AdaptiveTransitionSystem(
            ["red", "red/yellow", "green", "yellow"],
            ["switch"],
            ["red", "green", "yellow"],
            I=["green"],
        )
        ts1.add_transition("red", "switch", "red/yellow")
        ts1.add_transition("red/yellow", "switch", "green")
        ts1.add_transition("green", "switch", "yellow")
        ts1.add_transition("yellow", "switch", "red")

        ts1.add_label("red", "red")
        ts1.add_label("red/yellow", "red")
        ts1.add_label("red/yellow", "yellow")
        ts1.add_label("green", "green")
        ts1.add_label("yellow", "yellow")

        # Create dummy automaton
        aut1 = DeterministicRabinAutomaton(
            ["q0", "q1", "qF"],
            [set(elt) for elt in self.powerset(["red", "green", "yellow"])],
            ["q0"],
            F=[(set(["qF"]), set(["qF"]))],
        )
        # Add transitions for q0
        for sigma in aut1.Sigma:
            if ("yellow" in sigma) and ("red" not in sigma):
                aut1.add_transition("q0", sigma, "q1")
            if ("red" not in sigma) and ("yellow" not in sigma):
                aut1.add_transition("q0", sigma, "q0")
            if "red" in sigma:
                aut1.add_transition("q0", sigma, "qF")

        # Add transitions from q1
        for sigma in aut1.Sigma:
            if "yellow" in sigma:
                aut1.add_transition("q1", sigma, "q1")
            else:
                aut1.add_transition("q1", sigma, "q0")

        # Attempt to compute product
        product_ts = ts1.product(aut1)
        # print(product_ts.S)
        # assert len(product_ts.S) == 4
        assert len(product_ts.Act) == 1
        # for transition in product_ts.transitions:
        #     #print(transition)
        #     print((product_ts.S[transition[0]], product_ts.Act[transition[1]], product_ts.S[transition[2]]))
        assert len(product_ts.reachable_states_from(product_ts.I)) == 4, f"Expected 4 transitions, got {len(product_ts.transitions)} transitions."


if __name__ == "__main__":
    unittest.main()
