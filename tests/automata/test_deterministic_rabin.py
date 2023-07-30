"""
test_deterministic_rabin.py
Description:
    Tests the Deterministic Rabin Automaton class.
"""

import unittest

from kltl.automata import DeterministicRabinAutomaton

class TestDeterministicRabinAutomaton(unittest.TestCase):
    def test_add_accepting_pair1(self):
        """
        test_add_accepting_pair1
        Description:
            Tests that we can add an accepting pair to the automaton.
        :return:
        """

        # Create simple automaton
        dfa = DeterministicRabinAutomaton(
            Q=["s0", "s1", "s2"],
            Sigma=[set(), {"0"}, {"1"}, {"0", "1"}],
            Q0 = ["s0"],
        )

        # Add accepting pair
        dfa.add_accepting_pair(F_i={"s0"}, I_i={"s1", "s2"})

        # Check that the accepting pair was added
        self.assertEqual(dfa.F, [({"s0"}, {"s1", "s2"})])


if __name__ == '__main__':
    unittest.main()
