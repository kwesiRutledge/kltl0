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
            for theta in eta:
                for x_prime in system.post(x, u, theta):
                    for theta_prime in eta:
                        if x_prime in system.post(x, u, theta_prime):
                            gamma_xeta_u.append(theta_prime)



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
            # Observe all of the thetas (from our current eta) can explain x_prime
            for theta_prime in eta:
                if x_prime in system.post(x, u, theta_prime):
                    eta_prime.append(theta_prime)

            post_xeta_u.append((x_prime, eta_prime))

    return post_xeta_u
