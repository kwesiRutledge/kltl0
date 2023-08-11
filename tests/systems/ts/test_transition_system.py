"""
test_transition_system.py
Description:
    Testing that the transition system works.
"""
import unittest

from kltl.systems import (
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

        self.assertEqual(len(ts1.I), 0)

    def test_transition_system2(self):
        ts3 = TransitionSystem(
            ["s1", "s2", "s3"], ["a1", "a2"], ["p1", "p2", "p3"],
        )

        # Assert
        self.assertEqual(len(ts3.transitions), 0)

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

    def test_add_label1(self):
        ts1 = TransitionSystem(
            ["s1", "s2", "s3"], ["a1", "a2"], ["p1", "p2", "p3"],
        )

        # Check that the transition system is empty
        self.assertEqual(
            len(TransitionSystem(["s1", "s2", "s3"], ["a1", "a2"], ["p1", "p2", "p3"]).labels),
            0,
        )

        # Add a transition
        ts1.add_label("s1", "p1")
        ts1.add_label("s1", "p2")

        # Check that the transition set has one element
        self.assertEqual(ts1.labels.shape[0], 2)
        self.assertEqual(
            ts1.L("s1"), ["p1", "p2"],
        )

    def test_add_transition1(self):
        ts1 = TransitionSystem(
            ["s1", "s2", "s3"], ["a1", "a2"], ["p1", "p2", "p3"],
        )

        # Check that the transition system is empty
        self.assertEqual(len(ts1.labels), 0)

        # Add a transition
        ts1.add_transition("s1", "a1", "s2")
        ts1.add_transition("s1", "a2", "s3")

        # Check that the transition set has one element
        self.assertEqual(len(ts1.transitions), 2)
        self.assertEqual(
            ts1.post("s1"), ["s2", "s3"],
        )

    def test_to_networkx_graph1(self):
        """
        test_to_networkx_graph1
        Description:
            Tests how well the conversion from our representation to a networkx graph works.
            IS it better to use their representation?
        :return:
        """
        ts1 = TransitionSystem(
            ["s1", "s2", "s3"], ["a1", "a2"], ["p1", "p2", "p3"],
        )

        # Add a transition
        ts1.add_transition("s1", "a1", "s2")
        ts1.add_transition("s1", "a2", "s3")

        # Convert to networkx graph
        graph = ts1.to_networkx_graph()

        # Check that the transition set has one element
        self.assertEqual(len(graph.nodes), 3)
        self.assertEqual(len(graph.edges), 2)

    def test_find_action_sequence_that_explains_state_sequence1(self):
        """
        test_find_action_sequence_that_explains_state_sequence1
        Description:
            Tests that the state recovery works for a simple example (sequence contains one element.
        :return:
        """
        ts1 = TransitionSystem(
            ["s1", "s2", "s3"], ["a1", "a2"], ["p1", "p2", "p3"],
        )

        # Add a transition
        ts1.add_transition("s1", "a1", "s2")
        ts1.add_transition("s1", "a2", "s1")
        ts1.add_transition("s2", "a1", "s3")
        ts1.add_transition("s2", "a2", "s1")
        ts1.add_transition("s3", "a1", "s3")
        ts1.add_transition("s3", "a2", "s2")

        # Find the action sequence that explains the state sequence
        a = ts1.find_action_sequence_that_explains_state_sequence(["s1"])
        self.assertEqual(a, [])

        a = ts1.find_action_sequence_that_explains_state_sequence([])
        self.assertEqual(a, [])

    def test_find_action_sequence_that_explains_state_sequence2(self):
        """
        test_find_action_sequence_that_explains_state_sequence2
        Description:
            Tests that the state recovery works for a simple example (sequence contains more than one element).
        :return:
        """
        ts1 = TransitionSystem(
            ["s1", "s2", "s3"], ["a1", "a2"], ["p1", "p2", "p3"],
        )

        # Add a transition
        ts1.add_transition("s1", "a1", "s2")
        ts1.add_transition("s1", "a2", "s1")
        ts1.add_transition("s2", "a1", "s3")
        ts1.add_transition("s2", "a2", "s1")
        ts1.add_transition("s3", "a1", "s3")
        ts1.add_transition("s3", "a2", "s2")

        # Find the action sequence that explains the state sequence
        a = ts1.find_action_sequence_that_explains_state_sequence(["s1", "s2"])
        self.assertEqual([ts1.Act[int(i)] for i in a], ["a1"])

        a = ts1.find_action_sequence_that_explains_state_sequence(["s1", "s2", "s3"])
        self.assertEqual([ts1.Act[int(i)] for i in a], ["a1", "a1"])

        a = ts1.find_action_sequence_that_explains_state_sequence(["s1", "s2", "s3", "s3", "s2"])
        self.assertEqual([ts1.Act[int(i)] for i in a], ["a1", "a1", "a1", "a2"])

if __name__ == '__main__':
    unittest.main()