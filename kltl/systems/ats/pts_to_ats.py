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
    U = system.Act

    # Construct new X
    X_adp_new = [ (x, system.Theta) for x in system.X ]
    X_adp = X_adp_new

    # Loop until X_adp_new is empty
    while len(X_adp_new) > 0:
        X_adp_new = []
        for (x, eta) in X_adp:
            for u in U:
                gamma_xeta_u = []
                eta_prime = []
                succ_tuples = collect_all_successors_that_can_follow_from(system, x, eta, u)

                # Add the novel states to X_adp
                for (x_prime, eta_prime) in succ_tuples:
                    if (x_prime, eta_prime) not in X_adp:
                        X_adp_new.append((x_prime, eta_prime))
                        X_adp.append((x_prime, eta_prime))

    # When done create system using X_adp
    ats_out = AdaptiveTransitionSystem(
        X_adp, system.Act, system.AP,
        I=[(x, system.Theta) for x in system.I],
    )

    # Add outputs for each state
    for (x, eta) in X_adp:
        ats_out.add_label((x, eta), system.L(x))

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
        for x_prime in system.post(x, u, theta):
            eta_prime = []
            # Observe all of the thetas (from our current eta) that can explain x_prime
            for theta_prime in eta:
                if x_prime in system.post(x, u, theta_prime):
                    eta_prime.append(theta_prime) if theta_prime not in eta_prime else None

            if (x_prime, eta_prime) not in post_xeta_u:
                post_xeta_u.append((x_prime, eta_prime))

    return post_xeta_u
