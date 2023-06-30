"""
traces.py
Description:
    A module for handling traces in a transition system.
"""

from typing import List, Tuple, Union
from kltl.types import AtomicProposition

from kltl.systems.transition_system import TransitionSystem

class FiniteTrace:
    """
    FiniteTrace
    Description:
        This class represents a finite trace in a transition system. (Almost like a finite length List[List[AtomicProposition]])
    """
    def __init__(self, trace_list: List[List[AtomicProposition]], system: TransitionSystem):
        # Input Processing
        assert len(trace_list) > 0

        self.trace_list = trace_list
        self.system = system

    def __len__(self):
        return len(self.trace_list)

    def __getitem__(self, idx):
        assert idx >= 0 and idx < len(self.trace_list), f"Index {idx} is out of bounds for trace of length {len(self.trace_list)}!"
        return self.trace_list[idx]



class InfiniteTrace:
    """
    InfiniteTrace
    Description:
        This class represents an infinite trace in a transition system. (Almost like an infinite length List[List[AtomicProposition]])
    """
    def __init__(self, prefix: List[List[AtomicProposition]], suffix: List[List[AtomicProposition]], system: TransitionSystem):
        # Input Processing
        assert len(suffix) > 0
        # assert len(suffix) % 2 == 1, f"Trajectory should have an odd number of entries, but found {len(trajectory_string)}!"

        # Parse the infinite trace into the part that is finite (prefix) and the part that is infinitely repeating
        self.prefix, self.repeating_suffix = prefix, suffix

        self.system = system

    def __getitem__(self, idx):
        # Check if the index is in the prefix
        if idx < len(self.prefix):
            return self.prefix[idx]
        else:
            # Get the index in the suffix
            idx = idx - len(self.prefix)
            idx = idx % len(self.repeating_suffix)

            # Return the element in the repeating suffix
            return self.states[idx]