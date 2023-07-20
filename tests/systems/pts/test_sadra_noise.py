"""
test_sadra_noise.py
Description:
    Tests the noisy version of Sadra's system.
"""

import unittest

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

if __name__ == '__main__':
    unittest.main()