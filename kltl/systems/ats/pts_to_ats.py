"""
pts_to_ats.py
Description:
    Defines Algorithm 1 from Sadra's paper.
"""
from typing import List, Tuple

from kltl.systems.pts import ParametricTransitionSystem
from kltl.systems.pts.pts_types import State, Action, Parameter
from .adaptive_transition_system import AdaptiveTransitionSystem

def pts2ats(system: ParametricTransitionSystem) -> AdaptiveTransitionSystem:
    """
    pts2ats
    Description:
        Converts a PTS to an ATS.
    :param system:
    :return:
    """
    # Constants
    Act = system.Act

    # Construct new S
    S_adp_new = [(s, system.Theta) for s in system.I]
    S_adp = S_adp_new
    transitions = []

    # Loop until S_adp_new is empty
    while len(S_adp_new) > 0:
        S_adp_new = []
        for (s, eta) in S_adp:
            for act in Act:
                eta_prime = []
                succ_tuples = collect_all_successors_that_can_follow_from(system, s, eta, act)

                # Add the novel states to S_adp
                for (s_prime, eta_prime) in succ_tuples:
                    if (s_prime, eta_prime) not in S_adp:
                        S_adp_new.append((s_prime, eta_prime))
                        S_adp.append((s_prime, eta_prime))

                # Add transitions from this state and action
                for (s_prime, eta_prime) in succ_tuples:
                    transitions.append(
                        ((s, eta), act, (s_prime, eta_prime))
                    )

    # When done create system using S_adp
    ats_out = AdaptiveTransitionSystem(
        S_adp, system.Act, system.AP,
        I=[(s, system.Theta) for s in system.I],
    )

    # Add transitions
    for transition in transitions:
        ats_out.add_transition(transition[0], transition[1], transition[2])

    # Add outputs for each state
    for (s, eta) in S_adp:
        L_s = system.L(s)
        if len(L_s) > 0:
            [ats_out.add_label((s, eta), L_s[k]) for k in range(len(L_s))]

    return ats_out

def collect_all_successors_that_can_follow_from(
    system, x: State, eta: List[Parameter], u: Action,
) -> List[Tuple[State, List[Parameter]]]:
    """
    collect_all_successors_that_can_follow_from
    Description:
        Collects all ATSStates that can follow from a given state-estimate pair with a given action.
    :param system:
    :param x:
    :param eta:
    :param u:
    :return:
    """
    # Setup
    post_xeta_u = []
    eta_prime = []

    # Main loop
    for theta in eta:
        for s_prime in system.post(x, u, theta):
            eta_prime = []
            # Observe all of the thetas (from our current eta) that can explain s_prime
            for theta_prime in eta:
                if s_prime in system.post(x, u, theta_prime):
                    eta_prime.append(theta_prime) if theta_prime not in eta_prime else None

            if (s_prime, eta_prime) not in post_xeta_u:
                post_xeta_u.append((s_prime, eta_prime))

    return post_xeta_u
