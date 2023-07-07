"""
test_sadra.py
Description:
    Tests some of the features of the sadradinni system.
"""
import os
import unittest

from kltl.systems.pts.sadra import get_sadra_system

import matplotlib.pyplot as plt

from kltl.systems.pts.trajectory import create_random_trajectory_with_N_actions


class TestSadra(unittest.TestCase):
    def test_get_sadra_system1(self):
        """
        test_get_sadra_system1
        Description:
            Tests that our method for getting the sadra system.
        :return:
        """
        # Constants
        sadra = get_sadra_system()

        # Test
        self.assertTrue(
            f"s_(0,0)" in sadra.S,
        )

        for s_i in sadra.S:
            self.assertTrue(s_i == sadra.O(s_i, "Windy")[0])
            self.assertTrue(s_i == sadra.O(s_i, "NoWind")[0])

    def test_plot1(self):
        """test plotting function first"""
        # Constants
        sadra = get_sadra_system()
        # fig = plt.figure()
        fig, ax = plt.subplots(1, 1)
        sadra.plot(f"s_(0,0)", ax=ax)

        os.makedirs("figures", exist_ok=True)
        fig.savefig("figures/sadra_plot1.png")

    def test_plot_trajectory1(self):
        # Constants
        sadra = get_sadra_system()

        # Sample Trajectory
        traj0 = create_random_trajectory_with_N_actions(sadra, 10)

        fig, ax = plt.subplots(1, 1)
        sadra.plot_trajectory(traj0, ax=ax)

        os.makedirs("figures", exist_ok=True)
        fig.savefig("figures/sadra_plot_trajectory1.png")


if __name__ == '__main__':
    unittest.main()