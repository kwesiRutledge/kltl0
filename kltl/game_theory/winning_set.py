"""
winning_set.py
Description:
    A library for computing the winning set of a reachability game on a transtion system.
"""

from typing import List, Set, Tuple, Union

import numpy as np

from kltl.systems import TransitionSystem, AdaptiveTransitionSystem
from kltl.types import State, Action, AtomicProposition, Transition

System = Union[TransitionSystem, AdaptiveTransitionSystem]

def winning_set_reachability(system: System, target_set: List[State]):
    """
    set, pol = winning_set_reachability(ts, target_set)
    Description:
        Computes the winning set of a reachability game on a transition system.
    :param system:
    :param target_set:
    :return:
    """
    # Constants

    # Algorithm
    # 1. Initialize the winning set to be the target set.
    target_set_indices = [system.S.index(s) for s in target_set]
    winning_set_k = []
    winning_set_kp1 = target_set_indices

    # 2. Initialize the policy to be empty.
    policy = {}

    # 3. While the winning set is changing:
    while winning_set_k != winning_set_kp1:
        # 3.1. Update the winning set.
        winning_set_k = winning_set_kp1

        # 3.2. For all states outside of the winning set:
        for s in system.S:
            if s in winning_set_k:
                continue

            # 3.2.1. Find an action that is guaranteed to reach the winning set.
            for a in system.Act:
                post_s_a = system.post_indices(s, a)
                # print(post_s_a)
                # print(winning_set_k)
                # print("intersect", np.intersect1d(post_s_a, winning_set_k))
                post_in_winning_set = np.intersect1d(post_s_a, winning_set_k)
                if len(post_in_winning_set) == 0:
                    continue

                if np.all(np.in1d(post_s_a, post_in_winning_set)):
                    s_index = system.S.index(s)
                    if policy.get(s_index) is None:
                        policy[s_index] = []
                    if a not in policy[s_index]:
                        policy[s_index].append(a)
                    # Add s to the winning set if it is not already yet.
                    if system.S.index(s) not in winning_set_kp1:
                        winning_set_kp1.append(system.S.index(s))
                    break

        # Clean up winning set
        winning_set_kp1 = list(set(winning_set_kp1))


    return [system.S[s_index] for s_index in winning_set_kp1], policy

def winning_set_reach_avoid(system: System, target_set: List[State], avoid_set: List[State]):
    """
    set, pol = winning_set_reachability(ts, target_set)
    Description:
        Computes the winning set of a reachability game on a transition system.
    :param system:
    :param target_set:
    :return:
    """
    # Constants

    # Algorithm
    # 1. Initialize the winning set to be the target set.
    target_set_indices = [system.S.index(s) for s in target_set]
    avoid_set_indices = [system.S.index(s) for s in avoid_set]
    winning_set_k = []
    winning_set_kp1 = target_set_indices

    # 2. Initialize the policy to be empty.
    policy = {}

    # 3. While the winning set is changing:
    while winning_set_k != winning_set_kp1:
        # 3.1. Update the winning set.
        winning_set_k = winning_set_kp1

        # 3.2. For all states outside of the winning set:
        for s in system.S:
            if (s in winning_set_k) or (s in avoid_set):
                continue

            # 3.2.1. Find an action that is guaranteed to reach the winning set.
            for a in system.Act:
                post_s_a = system.post_indices(s, a)
                # print(post_s_a)
                # print(winning_set_k)
                # print("intersect", np.intersect1d(post_s_a, winning_set_k))
                post_in_winning_set = np.intersect1d(post_s_a, winning_set_k)
                post_in_avoid_set = np.intersect1d(post_s_a, avoid_set_indices)
                if len(post_in_winning_set) == 0:
                    continue

                #print("post_in_avoid_set", post_in_avoid_set)
                if len(post_in_avoid_set) > 0:
                    continue

                if np.all(np.in1d(post_s_a, post_in_winning_set)):
                    s_index = system.S.index(s)
                    if policy.get(s_index) is None:
                        policy[s_index] = []
                    if a not in policy[s_index]:
                        policy[s_index].append(a)
                    # Add s to the winning set if it is not already yet.
                    if system.S.index(s) not in winning_set_kp1:
                        winning_set_kp1.append(system.S.index(s))
                    break

        # Clean up winning set
        winning_set_kp1 = list(set(winning_set_kp1))


    return [system.S[s_index] for s_index in winning_set_kp1], policy
