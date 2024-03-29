"""
test_policies.py
Description:
    Tests the control policies for the Sandra Sadradinni system, and the trajectories possible with them.
"""
import unittest

from kltl.systems.pts.sadra import get_sadra_system
from kltl.systems.pts.policies import ControlPolicies, get_all_trajectories

class TestSadraPolicies(unittest.TestCase):
    def test_policy1(self):
        sadra = get_sadra_system()
        initial_traj_sadra = sadra.I * 2

        policies = ControlPolicies(1)
        policy1 = policies.control_policy_1

        print(get_all_trajectories(policy1, 50, sadra))

    def test_policy2(self):
        sadra = get_sadra_system()
        initial_traj_sadra = sadra.I*2

        policies = ControlPolicies(1)
        policy2 = policies.control_policy_2

        print(get_all_trajectories(policy2, 50, sadra))

    def test_policy3(self):
        sadra = get_sadra_system()
        initial_traj_sadra = sadra.I*2

        policies = ControlPolicies(1)
        # policy1 = policies.control_policy_1
        # policy2 = policies.control_policy_2
        policy3 = policies.control_policy_3

        # print(get_all_trajectories(policy1, 50, sadra))
        # print(get_all_trajectories(policy2, 50, sadra))
        print(get_all_trajectories(policy3, 50, sadra))

if __name__ == "__main__":
    unittest.main()