"""
test_traces.py
Description:
    Tests the functions and classes defined in the traces module.
"""

import unittest

import

class TestTraces(unittest.TestCase):
    def test_trajectory1(self):
        # Create basic trajectory
        traj = Trajectory(
            ["state1", "action1", "state2"],
        )

        self.assertEqual(
            traj.s(0), "state1",
        )
        self.assertEqual(traj.s[1], "state2")
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()