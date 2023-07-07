"""
test_parametric_transition_system.py
Description:
    Tests some of the functions of the parametric transition system.
"""

import unittest

from kltl.systems.pts import ParametricTransitionSystem

class TestParametricTransitionSystem(unittest.TestCase):
    def test_O1(self):
        """
        test_O1
        Description:
            Tests the output method.
        :return:
        """
        # Constants
        S = ["s1", "s2", "s3", "s4", "s5"]
        Act = ["a1"]
        AP = ["ap1"]
        Theta = ["theta1", "theta2"]
        I = ["s1"]
        Y = ["o1", "o2", "o3"]

        # Define PTS
        sys = ParametricTransitionSystem(
            S, Act, AP,
            I=I, Y=Y, Theta=Theta,
        )

        # Add transitions
        sys.add_transition("s1", "a1", "theta1", "s2")
        sys.add_transition("s1", "a1", "theta2", "s3")
        sys.add_transition("s2", "a1", "theta1", "s4")
        sys.add_transition("s3", "a1", "theta2", "s5")
        sys.add_transition("s4", "a1", "theta1", "s1")
        sys.add_transition("s5", "a1", "theta2", "s1")

        # Add outputs
        sys.add_output("s1", Theta[0], "o1")
        sys.add_output("s1", Theta[1], "o1")
        sys.add_output("s2", Theta[0], "o2")
        sys.add_output("s3", Theta[1], "o2")
        sys.add_output("s4", Theta[0], "o2")
        sys.add_output("s5", Theta[1], "o3")

        # Add Labels
        sys.add_label("s4", AP[0])

        # Compute the outputs fo state s1 (there should be only one!)
        self.assertEqual(
            len(sys.O("s1")), 1,
        )

if __name__ == '__main__':
    unittest.main()