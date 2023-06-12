"""
test_transition_system.py
Description:
    Testing that the transition system works.
"""
import unittest

from kltl0.transition_system import (
    TransitionSystem,
)

class TestTransitionSystem(unittest.TestCase):
    def test_transition_system1(self):
        ts1 = TransitionSystem(
            ["s1", "s2", "s3"], ["a1", "a2"], ["p1", "p2", "p3"],
        )

        # Assert
        self.assertEqual(len(ts1.S), 3)
        self.assertEqual(len(ts1.Act), 2)
        self.assertEqual(len(ts1.AP), 3)

        self.assertEqual(len(ts1.I), 1)

    def test_transition_system2(self):
        ts2 = TransitionSystem(
            ["s1", "s2", "s3"], ["a1", "a2"], ["p1", "p2", "p3"],
        )

        # Assert
        self.assertEqual(len(ts2.transitions), 0)

    def test_add_transition1(self):
        ts1 = TransitionSystem(
            ["s1", "s2", "s3"], ["a1", "a2"], ["p1", "p2", "p3"],
        )

        # Check that the transition system is empty
        self.assertEqual(len(ts1.transitions), 0)

        # Add a transition
        ts1.add_transition("s1", "a1", "s2")

        # Check that the transition set has one element
        self.assertEqual(len(ts1.transitions), 1)
        self.assertEqual(
            ts1.transitions[0], (0, 0, 1),
        )


if __name__ == '__main__':
    unittest.main()