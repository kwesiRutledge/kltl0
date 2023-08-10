"""
graph_utils.py
"""

from typing import List, Set, Tuple, Union

import numpy as np


# from . import TransitionSystem, AdaptiveTransitionSystem
#
# System = Union[TransitionSystem, AdaptiveTransitionSystem]

def subset_of_system_connected_to_initial(system):
    """
    subset_of_system_connected_to_initial
    Description:
        Finds the states and transitions connected to the initial states.
    :param system:
    :return:
    """
    # Constants

    # Algorithm

def transition_matrix2adjacency_matrix(system):
    """
    transition_matrix2adjacency_matrix
    Description:
        Creates an adjacency matrix from the transition matrix defined in a transition system of some kind.
    :param system:
    :return:
    """
    # Constants

    # Algorithm
    compressed_tm = system.transitions[:, [0, -1]]
    adjacency_matrix = np.zeros((len(system.S), len(system.S)), dtype=int)
    adjacency_matrix[compressed_tm[:, 0], compressed_tm[:, 1]] = 1

    return adjacency_matrix


