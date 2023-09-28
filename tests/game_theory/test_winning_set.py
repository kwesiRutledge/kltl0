"""
test_winning_set.py
Description:
    Testing that the winning set algorithm works.
"""
import unittest

from kltl.game_theory.winning_set import winning_set_reachability
from kltl.systems import TransitionSystem


class TestWinningSet(unittest.TestCase):
    def get_completely_reachable_ts1(self):
        """
        ts = self.get_completely_reachable_ts1()
        :return:
        """
        # Constants
        S = ["s0", "s1", "s2", "s3"]
        Act = ["a0", "a1"]
        AP = ["p0", "p1"]
        I = ["s0"]

        # Create TS
        ts = TransitionSystem(S, Act, AP, I=I)

        # Add Transitions
        ts.add_transition("s0", "a0", "s1")
        ts.add_transition("s0", "a1", "s3")
        ts.add_transition("s1", "a0", "s2")
        ts.add_transition("s1", "a1", "s0")
        ts.add_transition("s2", "a0", "s3")
        ts.add_transition("s2", "a1", "s1")
        ts.add_transition("s3", "a0", "s0")
        ts.add_transition("s3", "a1", "s2")

        # Add Labels
        ts.add_label("s0", "p0")
        ts.add_label("s1", "p0")
        ts.add_label("s2", "p0")
        ts.add_label("s3", "p1")

        return ts


    def test_winning_set_reachability1(self):
        """
        Description:
            Test that the winning set algorithm works.
        :return:
        """
        # Constants
        ts = self.get_completely_reachable_ts1()

        # Algorithm
        ws, pol_win = winning_set_reachability(ts, ["s3"])

        # Assertions
        #self.assertFalse(pol_win)
        self.assertEqual(["s0", "s1", "s2", "s3"], ws)

    def get_not_robustly_reachable_ts1(self):
        """
        ts = self.get_not_robustly_reachable_ts1()
        :return:
        """
        # Constants
        S = ["s0", "s1", "s2", "s3"]
        Act = ["a0"]
        AP = ["p0", "p1"]
        I = ["s0"]

        # Create TS
        ts = TransitionSystem(S, Act, AP, I=I)

        # Add Transitions
        ts.add_transition("s0", "a0", "s1")
        ts.add_transition("s1", "a0", "s2")
        ts.add_transition("s1", "a0", "s3")

        # Add Labels
        ts.add_label("s0", "p0")
        ts.add_label("s1", "p0")
        ts.add_label("s2", "p0")
        ts.add_label("s3", "p1")

        return ts

    def test_winning_set_reachability2(self):
        """
        Description:
            Test that the winning set algorithm works.
        :return:
        """
        # Constants
        ts = self.get_not_robustly_reachable_ts1()

        # Algorithm
        ws, pol_win = winning_set_reachability(ts, ["s3"])

        # Assertions
        self.assertEqual(["s3"], ws)

if __name__ == '__main__':
    unittest.main()