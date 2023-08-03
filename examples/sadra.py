"""
sadra.py
Description:
    Example showing how Sadra's system should work.
Notes:
    There are a number of tools which can e used to define dfas including:
    - http://ltlf2dfa.diag.uniroma1.it/dfa
"""

import os
import time
from itertools import combinations, chain

from kltl.automata import DeterministicRabinAutomaton
from kltl.grammar.kltl_semantics import (
    Eventually, Always, Not, And, KLTLFormula
)
from kltl.systems.ats.pts_to_ats import pts2ats
from kltl.systems.pts import ParametricTransitionSystem

from kltl.systems.pts.sadra import get_sadra_system
from kltl.systems.pts.trajectory import create_random_trajectory_with_N_actions


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return list(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))

def create_automaton_for_negation_of_task(sadra_system: ParametricTransitionSystem, phi: KLTLFormula) -> DeterministicRabinAutomaton:
    """
    dra_out = create_automaton_for_negation_of_task(sadra, phi)
    Description:
        Creates an automaton that can be used to
        Automaton is defined by giving the formula "!((G(!(a)) & F(b) & F(c)))" to the http://ltlf2dfa.diag.uniroma1.it/dfa
        tool.
    Recall:
        AP = ["Crashed!", "Surveil1", "Surveil2"]
    :param phi:
    :return:
    """
    # Constants
    AP = sadra_system.AP

    # Create the automaton
    dra = DeterministicRabinAutomaton(
        ["q1", "q2", "q3", "q4", "q5"],
        [set(elt) for elt in powerset(AP)],
        ["q1"],
        F=[(set(["q2", "q3", "q4"]), set(["q5"]))],
    )

    # Add transitions
    # Add transitions from q1
    for sigma in dra.Sigma:
        if sigma == set([]):
            dra.add_transition("q1", sigma, "q1")
        if sigma == set(["Surveil2"]):
            dra.add_transition("q1", sigma, "q2")
        if sigma == set(["Surveil1"]):
            dra.add_transition("q1", sigma, "q3")
        if "Crashed!" in sigma:
            dra.add_transition("q1", sigma, "q5")
        if sigma == set(["Surveil1", "Surveil2"]):
            dra.add_transition("q1", sigma, "q4")

    # Add transitions from q2
    for sigma in dra.Sigma:
        if ("Crashed!" not in sigma) and ("Surveil1" not in sigma):
            dra.add_transition("q2", sigma, "q2")
        if ("Crashed!" not in sigma) and ("Surveil1" in sigma):
            dra.add_transition("q2", sigma, "q4")
        if "Crashed!" in sigma:
            dra.add_transition("q2", sigma, "q5")

    # Add transitions from q3
    for sigma in dra.Sigma:
        if ("Crashed!" not in sigma) and ("Surveil2" not in sigma):
            dra.add_transition("q3", sigma, "q3")
        if ("Crashed!" not in sigma) and ("Surveil2" in sigma):
            dra.add_transition("q3", sigma, "q4")
        if "Crashed!" in sigma:
            dra.add_transition("q3", sigma, "q5")

    # Add transitions from q4
    for sigma in dra.Sigma:
        if ("Crashed!" not in sigma):
            dra.add_transition("q4", sigma, "q4")
        if "Crashed!" in sigma:
            dra.add_transition("q4", sigma, "q5")

    # Add transitions from q5
    for sigma in dra.Sigma:
        dra.add_transition("q5", sigma, "q5")

    return dra

def main():
    # Get System
    sadra = get_sadra_system()
    print("Created Sadra Paramteric Transition System with {} columns and {} rows.".format(sadra.n_cols, sadra.n_rows))

    # Attempt to Sample Trajectories of the system
    n_trajs = 10
    traj0 = create_random_trajectory_with_N_actions(sadra, n_trajs)
    # print(traj0)
    print(f"Sampled {n_trajs} trajectories from sadra system.")

    # Convert Sadra PTS to an ATS
    print("Converting Sadra PTS to an ATS...")

    conversion_start = time.time()
    sadra_ats = pts2ats(sadra)
    conversion_end = time.time()

    print(f"- Converted Sadra PTS to an ATS with:")
    print(f"  + {len(sadra_ats.S)} states")
    print(f"  + {len(sadra_ats.I)} initial states")
    print(f"  + {len(sadra_ats.transitions)} transitions")
    print(f"- Conversion took {conversion_end - conversion_start} seconds.")

    # Create task for avoiding the unsafe states and eventually reaching the goal
    phi = And(
        Always(Not(sadra.AP[0])),
        And(Eventually(sadra.AP[1]), Eventually(sadra.AP[2])),
    )

    # Create automaton for the negation of this task
    dra_out = create_automaton_for_negation_of_task(sadra, phi)
    print(f"Created automaton for negation of task which contains {len(dra_out.Q)} states and {len(dra_out.transitions)} transitions.")

    # Compute product of these two
    print("Computing product of the ATS and the automaton for the negation of the task...")
    product_start = time.time()
    sadra_ats_product = sadra_ats.product(dra_out)
    product_end = time.time()
    print(f"- Product of the ATS and the automaton for the negation of the task contains")
    print(f"  + {len(sadra_ats_product.S)} states,")
    print(f"  + {len(sadra_ats_product.I)} initial states,")
    print(f"  + {len(sadra_ats_product.transitions)} transitions.")
    print(f"- Product took {product_end - product_start} seconds to compute.")




if __name__ == '__main__':
    main()
