"""
test_pts_to_ats.py
Description:
    Tests the functions of this file.
"""
import unittest

import numpy as np

from kltl.systems.ats.pts_to_ats import collect_all_successors_that_can_follow_from, pts2ats
import kltl.systems.pts.sadra as sadra_og
import kltl.systems.pts.sadra_noise as sadra_noise

class TestPTS2ATS(unittest.TestCase):
    def test_collect_all_successors_that_can_follow_from1(self):
        # Setup
        system = sadra_og.get_sadra_system()
        s = "s_(4,4)"

        # Add noise to system's transitions
        coords = system.state_name_to_coordinates(s)
        for theta in system.Theta:
            system.add_transition(s, "up", theta, f"s_({coords[0] + 1},{coords[1] + int(theta)})")
            system.add_transition(s, "up", theta, f"s_({coords[0] + 1},{coords[1] + int(theta) + 1})")
            system.add_transition(s, "up", theta, f"s_({coords[0] + 1},{coords[1] + int(theta) - 1})")
            # Down
            system.add_transition(s, "down", theta, f"s_({coords[0] - 1},{coords[1] + int(theta)})")
            system.add_transition(s, "down", theta, f"s_({coords[0] - 1},{coords[1] + int(theta) - 1})")
            system.add_transition(s, "down", theta, f"s_({coords[0] - 1},{coords[1] + int(theta) + 1})")
            # Left
            system.add_transition(s, "left", theta, f"s_({coords[0]},{coords[1] + int(theta) - 1})")
            system.add_transition(s, "left", theta, f"s_({coords[0]},{np.maximum(coords[1] + int(theta) - 1 - 1, 0)})")
            system.add_transition(s, "left", theta, f"s_({coords[0]},{coords[1] + int(theta) - 1 + 1})")
            # Right
            system.add_transition(s, "right", theta, f"s_({coords[0]},{coords[1] + int(theta) + 1})")
            system.add_transition(s, "right", theta, f"s_({coords[0]},{coords[1] + int(theta) + 1 - 1})")
            system.add_transition(s, "right", theta, f"s_({coords[0]},{coords[1] + int(theta) + 1 + 1})")

        # Check to see that there are multiple successors for this state in the noise.
        for theta in system.Theta:
            # print(theta)
            # print(system.post(s, "up", theta))
            self.assertTrue(len(system.post(s, "up", theta)) > 1)

        succ1 = collect_all_successors_that_can_follow_from(system, s, system.Theta, "right")
        self.assertGreater(len(succ1), 0)

        # print(succ1)

    def test_pts2ats1(self):
        """
        test_pts2ats1
        Description:
            Tests that the PTS2ATS function works correctly by using it on the Sadra system.
        :return:
        """
        # Constants
        system = sadra_og.SadraSystem(
            n_cols=5,
        )

        # Algorithm
        ats = pts2ats(system)
        print("Created adaptive transition system with:")
        print(f"{len(ats.S)} states")
        print(f"{len(ats.transitions)} transitions")
        print(f"{len(ats.I)} initial states")
        print(f"{len(ats.Act)} actions")

        self.assertGreater(len(ats.transitions), 0)
        self.assertGreater(len(ats.labels), 0)
        self.assertGreater(len(ats.I), 0)
        self.assertGreater(len(ats.Act), 0)
        self.assertGreater(len(ats.S), 0)
        self.assertGreater(len(ats.AP), 0)

if __name__ == '__main__':
    unittest.main()