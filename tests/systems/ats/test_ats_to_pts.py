"""
test_pts_to_ats.py
Description:
    Tests the functions of this file.
"""
import unittest

from kltl.systems.pts.sadra import get_sadra_system
from kltl.systems.pts.sadra_noise import SadraSystem


class TestPTS2ATS(unittest.TestCase):
    def test_collect_all_successors_that_can_follow_from1(self):
        # Setup
        system = SadraSystem()
        s = "s_(4,4)"

        # Check to see that there are multiple successors for this state in the noise.
        for theta in system.Theta:
            print(theta)
            print(system.post(s, "up", theta))
            self.assertTrue(len(system.post(s, "up", theta)) > 1)




        pass

if __name__ == '__main__':
    unittest.main()