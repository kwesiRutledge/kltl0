"""
test_trajectory.py
Description:
    Tests the PTS's trajectory module.
"""
import unittest

from kltl.systems.pts import (
    ParametricTransitionSystem,
    FiniteTrajectory, InfiniteTrajectory,
)

class TestTrajectory(unittest.TestCase):
    def test_InfiniteTrajectory_s1(self):
        """
        test_InfiniteTrajectory_s1
        Description:
            Tests that we can retrieve the proper outputs out of an infinite trajectory object.
        :return:
        """