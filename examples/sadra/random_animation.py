import ipdb
import typer

import os
import matplotlib.pyplot as plt

from kltl.systems.pts.sadra import get_sadra_system
from kltl.systems.pts.trajectory import create_random_trajectory_with_N_actions

def main():
    # Constants
    sadra = get_sadra_system()
    filename = "figures/animated_random_trajectory1.gif"

    # Create
    os.makedirs("figures", exist_ok=True)

    # Sample Trajectory
    traj0 = create_random_trajectory_with_N_actions(sadra, 10)

    fig, ax = plt.subplots(1, 1)
    sadra.save_animated_trajectory(traj0, filename, ax=ax)

if __name__ == '__main__':
    with ipdb.launch_ipdb_on_exception():
        typer.run(main)
