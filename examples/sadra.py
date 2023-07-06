"""
sadra.py
Description:
    Example showing how Sadra's system should work.
"""

import os

from kltl.systems.pts.sadra import get_sadra_system
from kltl.systems.pts.trajectory import create_random_trajectory_with_N_actions

def main():
    # Get System
    sadra = get_sadra_system()

    # Attempt to Sample Trajectories of the system
    traj0 = create_random_trajectory_with_N_actions(sadra, 10)
    print(traj0)



if __name__ == '__main__':
    main()