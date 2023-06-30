"""
test_traces.py
Description:
    Tests the functions and classes defined in the traces module.
"""

import unittest

from kltl.systems.ts import (
    get_beverage_vending_machine
)
from kltl.systems.ts import FiniteTrajectory, create_random_trajectory_with_N_actions

class TestTraces(unittest.TestCase):
    def test_trajectory1(self):
        # constants
        ts1 = get_beverage_vending_machine()

        # Create basic trajectory
        traj = FiniteTrajectory(
            ["start", "coin", "select"],
            ts1,
        )

        self.assertEqual(
            traj.s(0), "start",
        )
        self.assertEqual(traj.s(1), "select")
        self.assertTrue(True)

    def test_create_random_trajectory_of_length1(self):
        """
        Tests that a random trajectory of length 1 is created correctly.
        :return:
        """
        # constants
        ts1 = get_beverage_vending_machine()

        # Create random trajectory of length 1
        traj = create_random_trajectory_with_N_actions(ts1, 1)

        # Check that the trajectory is of length 1
        self.assertEqual(len(traj), 2)

if __name__ == "__main__":
    unittest.main()