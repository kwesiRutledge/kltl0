"""
control.py
Description:
    Example showing how Sadra's system should work.
Notes:
    There are a number of tools which can e used to define dfas including:
    - http://ltlf2dfa.diag.uniroma1.it/dfa
"""

import os
import time
from itertools import combinations, chain
from typing import Tuple, List

import ipdb
import networkx as nx
import numpy as np
import typer as typer
import yaml
from matplotlib import pyplot as plt
from yaml import Loader

from kltl.automata import DeterministicRabinAutomaton
from kltl.grammar.kltl_semantics import (
    Eventually, Always, Not, And, KLTLFormula
)
from kltl.systems import AdaptiveTransitionSystem, TransitionSystem
from kltl.systems.ats.pts_to_ats import pts2ats
from kltl.systems.pts import ParametricTransitionSystem

from kltl.systems.pts.sadra import get_sadra_system
from kltl.systems.pts.trajectory import create_random_trajectory_with_N_actions, FiniteTrajectory
from kltl.types import Action


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

def conversion_step(sadra_system: ParametricTransitionSystem, data_dir: str, force: bool = False) -> DeterministicRabinAutomaton:
    """
    ats, timing = conversion_step(sadra_system, data_dir)
    :param sadra_system:
    :param force: If True, then the conversion will be forced.
    :return:
    """
    # Constants
    sadra_ats_data_file = data_dir + 'sadra_ats.yml'

    # Algorithm
    conversion_time = -1.0
    do_conversion = not os.path.exists(sadra_ats_data_file)  # If the data file does not exist, then create a system.
    do_conversion = do_conversion or force  # Flag can be used to force conversion online.
    if do_conversion:
        conversion_start = time.time()
        sadra_ats = pts2ats(sadra_system)
        conversion_end = time.time()

        print(f"- Converted Sadra PTS to an ATS with:")
        print(f"  + {len(sadra_ats.S)} states")
        print(f"  + {len(sadra_ats.I)} initial states")
        print(f"  + {len(sadra_ats.transitions)} transitions")
        print(f"- Conversion took {conversion_end - conversion_start} seconds.")

        conversion_time = conversion_end - conversion_start

        # Save the data
        data_struct = {
            'S': sadra_ats.S,
            'AP': sadra_ats.AP,
            'Act': sadra_ats.Act,
            'I': sadra_ats.I,
            'transitions': sadra_ats.transitions,
            'labels': sadra_ats.labels,
            'conversion_time': conversion_time,
        }

        with open(sadra_ats_data_file, 'w') as f:
            yaml.dump(data_struct, f)
    else:
        with open(sadra_ats_data_file, 'r') as f:
            load_start = time.time()
            ats_data = yaml.load(f, Loader=Loader)

            sadra_ats = AdaptiveTransitionSystem(
                ats_data['S'],
                ats_data['Act'],
                ats_data['AP'],
                I=ats_data['I'],
                transitions=ats_data['transitions'],
                labels=ats_data['labels']
            )

            conversion_time = ats_data['conversion_time']
            load_end = time.time()

            print(f"- Loaded Sadra ATS from a previous computation.")
            print(f"  + The previous ATS contained:")
            print(f"    ~ {len(sadra_ats.S)} states")
            print(f"    ~ {len(sadra_ats.I)} initial states")
            print(f"    ~ {len(sadra_ats.transitions)} transitions")
            print(f"  + Conversion previously took {conversion_time} seconds.")
            print(f"  + The ATS was loaded via YAML in {load_end - load_start} seconds.")



    return sadra_ats, conversion_time

def product_step(
    sadra_ats: AdaptiveTransitionSystem,
    dra: DeterministicRabinAutomaton,
    data_dir: str,
    force: bool = False,
) -> Tuple[TransitionSystem, float]:
    # Constants
    sadra_product_data_file = data_dir + 'sadra_product.yml'

    # Algorithm
    product_time = -1.0
    compute_product = not os.path.exists(sadra_product_data_file)  # If the data file does not exist, then create a system.
    compute_product = compute_product or force  # Flag can be used to force conversion online.
    if compute_product:  # If the data file does not exist, then create a system.
        product_start = time.time()
        sadra_ats_product = sadra_ats.product(dra)
        product_end = time.time()
        print(f"- Product of the ATS and the automaton for the negation of the task contains")
        print(f"  + {len(sadra_ats_product.S)} states,")
        print(f"  + {len(sadra_ats_product.I)} initial states,")
        print(f"  + {len(sadra_ats_product.transitions)} transitions.")
        print(f"- Product took {product_end - product_start} seconds to compute.")

        product_time = product_end - product_start

        # Save the data
        data_struct = {
            'S': sadra_ats_product.S,
            'AP': sadra_ats_product.AP,
            'Act': sadra_ats_product.Act,
            'I': sadra_ats_product.I,
            'transitions': sadra_ats_product.transitions,
            'labels': sadra_ats_product.labels,
            'conversion_time': product_time,
        }

        with open(sadra_product_data_file, 'w') as f:
            yaml.dump(data_struct, f)

    else:
        with open(sadra_product_data_file, 'r') as f:
            load_start = time.time()
            product_ts_data = yaml.load(f, Loader=Loader)

            sadra_ats_product = TransitionSystem(
                product_ts_data['S'],
                product_ts_data['Act'],
                product_ts_data['AP'],
                I=product_ts_data['I'],
                transitions=product_ts_data['transitions'],
                labels=product_ts_data['labels']
            )

            conversion_time = product_ts_data['conversion_time']
            load_end = time.time()

            print(f"- Loaded Sadra Product TS from a previous computation.")
            print(f"  + The previous Product TS contained:")
            print(f"    ~ {len(sadra_ats_product.S)} states")
            print(f"    ~ {len(sadra_ats_product.I)} initial states")
            print(f"    ~ {len(sadra_ats_product.transitions)} transitions")
            print(f"  + Conversion previously took {conversion_time} seconds.")
            print(f"  + The ATS was loaded via YAML in {load_end - load_start} seconds.")

    return sadra_ats_product, product_time

def conversion_to_action_sequence_step(
        paths: List[List[int]],
        product_system: TransitionSystem,
        force: bool = False,
) -> Tuple[List[List[Action]], float]:
    """
    action_sequences, action_index_sequences, conversion_times = conversion_to_action_sequence_step(paths, product_ts)
    Description:
        Converts a list of action index sequences into a list of action sequences.
        (Loads the data if it can find some)
    :param action_index_sequences:
    :param force: bool; forces the algorithm to do conversion.
    :return:
    """
    # Constants
    action_sequences_data_file = 'data/action_sequences.yml'

    # Announcements
    print("Finding all action sequences for the given paths...")

    # Algorithm
    action_sequences, action_index_sequences = [], []
    conversion_times = []
    if not os.path.exists(action_sequences_data_file) or force:
        for path in paths:
            path_convert_start_i = time.time()
            action_index_sequence = product_system.find_action_sequence_that_explains_state_sequence(
                [product_system.S[i] for i in path]
            )
            action_sequence = [product_system.Act[i] for i in action_index_sequence]
            path_convert_end_i = time.time()

            # Update loop variables
            action_index_sequences.append(action_index_sequence)
            action_sequences.append(action_sequence)
            conversion_times.append(path_convert_end_i - path_convert_start_i)

        data_struct = {
            'action_sequences': action_sequences,
            'conversion_times': conversion_times,
        }

        print(f" - Converted all {len(paths)} paths to {len(action_sequences)} action sequences.")
        print(f" - Collected all action sequences in {np.array(conversion_times).sum()} seconds.")

        with open(action_sequences_data_file, 'w') as f:
            yaml.dump(data_struct, f)

        print(f" - Saving action sequences to {action_sequences_data_file}")

    else:
        with open(action_sequences_data_file, 'r') as f:
            load_start = time.time()
            action_sequence_data = yaml.load(f, Loader=Loader)

            action_sequences = action_sequence_data['action_sequences']
            conversion_times = action_sequence_data['conversion_times']

            load_end = time.time()
            print(f"- Loaded action sequences from a previous computation in {load_end - load_start} s.")
            print(f"- Previously collected all action sequences in {np.array(conversion_times).sum()} seconds.")

    return action_sequences, action_index_sequences, np.array(conversion_times).sum()

def main(force_pts_to_ats_conversion: bool = False, force_product_ts_creation: bool = False, force_action_sequence_conversion: bool = False):
    # Get System
    sadra = get_sadra_system()
    print("Created Sadra Paramteric Transition System with {} columns and {} rows.".format(sadra.n_cols, sadra.n_rows))

    # Create Data Directory and Figure Directories
    data_dir, fig_dir = './data/', './figures/'
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)

    # Attempt to Sample Trajectories of the system
    n_trajs = 10
    traj0 = create_random_trajectory_with_N_actions(sadra, n_trajs)
    # print(traj0)
    print(f"Sampled {n_trajs} trajectories from sadra system.")

    # Convert Sadra PTS to an ATS
    print("Converting Sadra PTS to an ATS...")
    sadra_ats, ats_conversion_time = conversion_step(sadra, data_dir, force=force_pts_to_ats_conversion)

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
    sadra_ats_product, product_time = product_step(sadra_ats, dra_out, data_dir, force=force_product_ts_creation)

    # Convert product ts to a graph
    print("Converting product TS to a graph...")
    networkx_construction_start = time.time()
    sadra_ats_product_graph = sadra_ats_product.to_networkx_graph()
    networkx_construction_end = time.time()
    print(f"- Conversion to a graph took {networkx_construction_end - networkx_construction_start} seconds.")
    print(f"- Final graph contains:")
    print(f"  + {len(sadra_ats_product_graph)} nodes")

    # Finding all paths to the target state
    print("Finding all paths to the target state...")
    label_indices_containing_full_sat = sadra_ats_product.labels[:, 1] == sadra_ats_product.AP.index('q4') # Q4 is reached only if all tasks are satisfied
    pathfind_times, num_paths_found, paths_found = [], 0, []
    for s in sadra_ats_product.labels[label_indices_containing_full_sat, 0]:
        #print("- Considering target state {}...".format(s))
        if not nx.has_path(sadra_ats_product_graph, 0, s):
            #print(" + State {} is not reachable from the initial state. Skipping".format(s))
            continue

        #print("  + Finding path to state {}...".format(s))
        pathfind_i_start = time.time()
        path = nx.shortest_path(sadra_ats_product_graph, 0, s)
        pathfind_i_end = time.time()

        # Report
        #print("    ~ Path to state {} contains {} states".format(s, len(path)))
        #print(f"    ~ Path to state {s} found in {pathfind_i_end - pathfind_i_start} seconds.")

        # Update list of data
        pathfind_times.append(pathfind_i_end - pathfind_i_start)
        paths_found.append(path)

    print(f"- Found {len(paths_found)} paths to states containing the full satisfaction of the task.")

    # Characterize which paths visit danger states
    print("Characterizing which paths visit danger states...")
    num_safe_paths_found = 0
    for path in paths_found:
        #print(f"- Considering path {path}...")
        # Find out if there are any labels for these elements of the path that have the danger albel
        states_labeled_dangerous = sadra_ats_product.labels[
            sadra_ats_product.labels[:, 1] == sadra_ats_product.AP.index("q5"), 0,
        ]
        dangerous_states_in_path = np.intersect1d(path, states_labeled_dangerous)

        if len(dangerous_states_in_path) > 0:
            # print(f"  + Path {path} contains dangerous states {dangerous_states_in_path}.")
            pass
        else:
            # print(f"  + Path {path} does not contain any dangerous states.")
            num_safe_paths_found += 1

    print(f"- Found {num_safe_paths_found} paths that do not contain any dangerous states.")

    action_sequences, action_index_sequences, conversion_times = conversion_to_action_sequence_step(
        paths_found, sadra_ats_product, force=force_action_sequence_conversion,
    )

    traj_str = []
    for i in range(len(action_sequences[0])):
        traj_str += [sadra_ats_product.S[path[i]][0][0], sadra_ats_product.S[path[i]][0][0], action_sequences[0][i]]

    traj_str += [sadra_ats_product.S[path[-1]][0][0], sadra_ats_product.S[path[-1]][0][0]]
    traj0 = FiniteTrajectory(traj_str, "+1", sadra)

    fig, ax = plt.subplots(1, 1)
    sadra.save_animated_trajectory(traj0, "figures/example_reaching_traj.gif", ax=ax)
    print(traj_str)
    print(" - Plotted one trajectory.")

    # for s in sadra_ats_product.S:
    #     print(s)
    #     if "Crashed!" in sadra.L(s[0][0]):
    #         print(s)

    # Find all paths that share the same action sequence (prefix)
    print("Finding all paths that share the same action sequence (prefix)...")
    n_prefixes_to_observe = 20
    matching_mat = np.zeros((len(action_index_sequences), n_prefixes_to_observe), dtype=int)
    for (i, action_index_sequence) in enumerate(action_index_sequences):
        print(f"- Considering action sequence #{i}...")
        for j in range(1, n_prefixes_to_observe): #range(len(action_index_sequence)):
            paths_with_this_action_sequence = []
            print(f"  + Checking prefix of length {j}...")

            if len(action_index_sequence) < j-1:
                print(f"    ~ Action sequence is too short. Skipping.")
                continue


            prefix = action_index_sequence[:j]
            for (k, action_index_sequence_inner) in enumerate(action_index_sequences):
                if i == k:
                    continue
                if len(action_index_sequence_inner) < j:
                    continue

                if np.all(prefix == action_index_sequence_inner[:j]):
                    paths_with_this_action_sequence.append(k)

            print(f"  ~ Found {len(paths_with_this_action_sequence)} paths with this action sequence prefix.")
            matching_mat[i, j] = len(paths_with_this_action_sequence)

    print(f"- Matching matrix is:")
    print(matching_mat)

    mm_fig = plt.figure()
    plt.imshow(matching_mat)
    plt.title("Prefix length histogram")
    plt.xlabel("Prefix length")
    plt.ylabel("Path index")



    # Find all cycles in the graph
    # print("Finding all cycles in the graph...")
    # state_containing_reach1 = np.argmax(label_indices_containing_full_sat)
    # cycles = nx.find_cycle(sadra_ats_product_graph, state_containing_reach1)
    # print(f"- {len(sorted(cycles))} cycles found in the graph.")
    # print(cycles)

if __name__ == '__main__':
    with ipdb.launch_ipdb_on_exception():
        typer.run(main)
