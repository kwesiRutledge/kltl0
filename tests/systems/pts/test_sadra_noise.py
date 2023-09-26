"""
test_sadra_noise.py
Description:
    Tests the noisy version of Sadra's system.
"""

import unittest
import matplotlib.pyplot as plt
import os

from kltl.systems.pts import FiniteTrajectory
from kltl.systems.pts.sadra_noise import SadraSystem

class TestSadraNoise(unittest.TestCase):
    def test_noisiness1(self):
        """
        TestNoisiness1
        Description:
            This test verifies that for each state in the windy region, there are more than one states
            that one can transition to.
        :return:
        """
        # Constants
        system = SadraSystem()

        x_i = "s_(4,4)"

        # Check to see that there are multiple successors for this state due to noise
        for theta in system.Theta:
            self.assertTrue(len(system.post(x_i, "up", theta)) > 1)
            self.assertTrue(len(system.post(x_i, "down", theta)) > 1)
            self.assertTrue(len(system.post(x_i, "left", theta)) > 1)
            self.assertTrue(len(system.post(x_i, "right", theta)) > 1)

    def test_len1(self):
        """
        test_len1
        Description:
            Tests that we can check the proper length of a trajectory.
        :return:
        """
        # Constants
        fig_dir = "figures/len1/"
        system = SadraSystem()

        # Create trajectory
        s_seq = [system.I[0], f"s_({system.n_cols-5},1)", f"s_({system.n_cols-5},2)", f"s_({system.n_cols-5},3)", f"s_({system.n_cols-5},4)"]
        a_seq = ["up", "up", "up", "up"]

        traj_str = []
        for (s_i, a_i) in zip(s_seq[:-1], a_seq):
            traj_str += [s_i, s_i, a_i]
        traj_str += [s_seq[-1], s_seq[-1]]

        ft = FiniteTrajectory(traj_str, "0", system)

        self.assertEqual(len(ft), 5)

    def test_plot_trajectory1(self):
        """
        test_plot_trajectory1
        Description:
            Tests that we can plot a trajectory.
        :return:
        """
        # Constants
        fig_dir = "figures/plot_trajectory1/"
        system = SadraSystem()

        # Create trajectory
        s_seq = [system.I[0], f"s_({system.n_cols-5},1)", f"s_({system.n_cols-5},2)", f"s_({system.n_cols-5},3)", f"s_({system.n_cols-5},4)"]
        a_seq = ["up", "up", "up", "up"]

        traj_str = []
        for (s_i, a_i) in zip(s_seq[:-1], a_seq):
            traj_str += [s_i, s_i, a_i]
        traj_str += [s_seq[-1], s_seq[-1]]

        ft = FiniteTrajectory(traj_str, "0", system)

        # Plot
        system.plot_trajectory(ft)

        traj_fig = plt.gcf()

        # If in correct directory, create this subdirectory
        if "tests/systems/pts" in os.getcwd():
            os.makedirs(fig_dir, exist_ok=True)
            traj_fig.savefig(fig_dir + "trajectory1.png")

    def test_plot_trajectory2(self):
        """
        test_plot_trajectory2
        Description:
            Tests that we can plot a trajectory.
        :return:
        """
        # Constants
        fig_dir = "figures/plot_trajectory2/"
        system = SadraSystem()

        # Create trajectory
        s_seq = [system.I[0], f"s_({system.n_cols-5},1)", f"s_({system.n_cols-5},2)", f"s_({system.n_cols-5},3)", f"s_({system.n_cols-4},4)"]
        a_seq = ["up", "up", "up", "up"]

        traj_str = []
        for (s_i, a_i) in zip(s_seq[:-1], a_seq):
            traj_str += [s_i, s_i, a_i]
        traj_str += [s_seq[-1], s_seq[-1]]

        ft = FiniteTrajectory(traj_str, "0", system)

        # Plot
        system.plot_trajectory(ft)

        traj_fig = plt.gcf()

        # If in correct directory, create this subdirectory
        if "tests/systems/pts" in os.getcwd():
            os.makedirs(fig_dir, exist_ok=True)
            traj_fig.savefig(fig_dir + "trajectory.png")

    def test_plot_trajectory2(self):
        """
        test_plot_trajectory2
        Description:
            Tests that we can plot a trajectory.
        :return:
        """
        # Constants
        fig_dir = "figures/plot_trajectory3/"
        system = SadraSystem()

        # Create trajectory
        s_seq = [system.I[0], f"s_({system.n_cols-5},1)", f"s_({system.n_cols-5},2)", f"s_({system.n_cols-5},3)", f"s_({system.n_cols-5-1},4)"]
        a_seq = ["up", "up", "up", "up"]

        traj_str = []
        for (s_i, a_i) in zip(s_seq[:-1], a_seq):
            traj_str += [s_i, s_i, a_i]
        traj_str += [s_seq[-1], s_seq[-1]]

        ft = FiniteTrajectory(traj_str, "0", system)

        # Plot
        system.plot_trajectory(ft)

        traj_fig = plt.gcf()

        # If in correct directory, create this subdirectory
        if "tests/systems/pts" in os.getcwd():
            os.makedirs(fig_dir, exist_ok=True)
            traj_fig.savefig(fig_dir + "trajectory.png")

if __name__ == '__main__':
    unittest.main()