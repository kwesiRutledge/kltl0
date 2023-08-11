"""
sadra_noise.py
Description:
    This file makes it easy to create your own version of Sadra Sadradinni's Parametric Transition System example from his
    "Formal methods for adaptive control of dynamical systems" paper.
"""
import numpy as np
from random import choice

from kltl.systems.pts import ParametricTransitionSystem, FiniteTrajectory

from typing import Tuple, Dict, Any
from kltl.types import State
from kltl.systems.pts.pts_types import Parameter

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import matplotlib.animation as manimation

class SadraSystem(ParametricTransitionSystem):
    def __init__(self, n_cols: int = 15, n_rows: int = 10, windy_region_y_lb: int = 3, windy_region_y_ub: int = 6):
        # Constants
        self.windy_region_y_lb = 3
        self.windy_region_y_ub = 6

        # Create state space
        self.n_cols = n_cols
        self.n_rows = n_rows
        S = [f"s_({col_idx},{row_idx})" for row_idx in range(n_rows) for col_idx in range(n_cols)]

        Act = ["up", "left", "right", "down"]  # Action Space
        Y = S  # Output Space
        AP = ["Crashed!", "Surveil1", "Surveil2"]  # Atomic Propositions
        Theta = ["-2", "-1", "0", "1", "2"]

        # Initial State set
        I = [f"s_({n_cols - 5},0)"]

        super().__init__(S, Act, AP, I=I, Y=Y, Theta=Theta)

        # Create the transitions
        for row_idx in range(n_rows):
            for col_idx in range(n_cols):
                for theta in self.Theta:
                    if (row_idx >= windy_region_y_lb) and (row_idx <= windy_region_y_ub):
                        self.add_transitions_for_shift(theta, (col_idx, row_idx))
                    else:
                        self.add_standard_transitions_for_mode("0", (col_idx, row_idx), n_rows, n_cols)
                        
        # Create the output map
        for row_idx in range(n_rows):
            for col_idx in range(n_cols):
                for theta in self.Theta:
                    self.add_output(f"s_({col_idx},{row_idx})", theta, f"s_({col_idx},{row_idx})")
                    self.add_output(f"s_({col_idx},{row_idx})", theta, f"s_({col_idx},{row_idx})")

        # Label Two regions as important recon points
        self.add_label(f"s_({n_cols-3},0)", "Surveil1")
        self.add_label(f"s_(2,{n_rows-1})", "Surveil2")
        for row_idx in range(n_rows):
            self.add_label(f"s_(0,{row_idx})", "Crashed!")
            self.add_label(f"s_({self.n_cols-1},{row_idx})", "Crashed!")

    def clamp_col(self, col_index: int) -> int:
        return max(0, min(col_index, self.n_cols-1))

    def clamp_row(self, row_index: int) -> int:
        return max(0, min(row_index, self.n_rows-1))

    def add_standard_transitions_for_mode(
            self,
            theta: Parameter,
            state_coords: Tuple[int],
            n_rows: int = 10, n_cols: int = 15,
    ):
        """
        add_adjacent_transitions_for_mode
        Description:

        :param self:
        :param theta: String representing the current parameter.
        :param s: tuple containing the row_index and col_index
        :return: Nothing. Transition systems hould be modified to
        """
        # Constants

        # Create string for state
        s_i = f"s_({state_coords[0]},{state_coords[1]})"

        # Add Transitions
        #if state_coords[0] != n_rows - 1:  # If current state is at the top of the space, it can not move north
        s_i_next = f"s_({state_coords[0]},{self.clamp_row(state_coords[1]+1)})"
        self.add_transition(s_i, "up", theta, s_i_next)

        s_i_next = f"s_({state_coords[0]},{self.clamp_row(state_coords[1]-1)})"
        self.add_transition(s_i, "down", theta, s_i_next)

        s_i_next = f"s_({self.clamp_col(state_coords[0]-1)},{state_coords[1]})"
        self.add_transition(s_i, "left", theta, s_i_next)

        s_i_next = f"s_({self.clamp_col(state_coords[0]+1)},{state_coords[1]})"
        self.add_transition(s_i, "right", theta, s_i_next)

    def add_transitions_for_shift(
        self,
        theta: Parameter,
        state_coords: Tuple[int],
    ):
        """
        add_adjacent_transitions_for_mode
        Description:

        :param ts:
        :param theta: String representing the current parameter.
        :param s: tuple containing the row_index and col_index
        :return: Nothing. Transition systems hould be modified to
        """
        # Constants
        shift = int(theta)
        n_rows, n_cols = self.n_rows, self.n_cols

        # Create string for state
        s_i = f"s_({state_coords[0]},{state_coords[1]})"

        # Add Transitions
        s_i_up = f"s_({self.clamp_row(state_coords[0] - 1)},{self.clamp_col(state_coords[1] - shift)})"
        self.add_transition(s_i, "up", theta, s_i_up)

        s_i_down = f"s_({self.clamp_row(state_coords[0] + 1)},{self.clamp_col(state_coords[1] - shift)})"
        self.add_transition(s_i, "down", theta, s_i_down)

        s_i_left = f"s_({state_coords[0]},{self.clamp_col(state_coords[1] - shift - 1)})"
        self.add_transition(s_i, "left", theta, s_i_left)

        s_i_right = f"s_({state_coords[0]},{self.clamp_col(state_coords[1] - shift + 1)})"
        self.add_transition(s_i, "right", theta, s_i_right)
        
        # Add Transitions for noise with greater disturbance
        shift += 1
        
        s_i_up = f"s_({self.clamp_row(state_coords[0] - 1)},{self.clamp_col(state_coords[1] - shift)})"
        self.add_transition(s_i, "up", theta, s_i_up)

        s_i_down = f"s_({self.clamp_row(state_coords[0] + 1)},{self.clamp_col(state_coords[1] - shift)})"
        self.add_transition(s_i, "down", theta, s_i_down)

        s_i_left = f"s_({state_coords[0]},{self.clamp_col(state_coords[1] - shift - 1)})"
        self.add_transition(s_i, "left", theta, s_i_left)

        s_i_right = f"s_({state_coords[0]},{self.clamp_col(state_coords[1] - shift + 1)})"
        self.add_transition(s_i, "right", theta, s_i_right)
        
        # Add Transitions for noise with less disturbance
        shift -= 1
        
        s_i_up = f"s_({self.clamp_row(state_coords[0] - 1)},{self.clamp_col(state_coords[1] - shift)})"
        self.add_transition(s_i, "up", theta, s_i_up)

        s_i_down = f"s_({self.clamp_row(state_coords[0] + 1)},{self.clamp_col(state_coords[1] - shift)})"
        self.add_transition(s_i, "down", theta, s_i_down)

        s_i_left = f"s_({state_coords[0]},{self.clamp_col(state_coords[1] - shift - 1)})"
        self.add_transition(s_i, "left", theta, s_i_left)

        s_i_right = f"s_({state_coords[0]},{self.clamp_col(state_coords[1] - shift + 1)})"
        self.add_transition(s_i, "right", theta, s_i_right)
        

    def state_name_to_coordinates(self, state: State)->Tuple[int, int]:
        """
        state_name_to_coordinates
        Description
            Converts the string representing the current state to the coordinates (tuple of integers)
        :param state:
        :return:
        """
        # Constants

        # Parse
        row_idx = int(state[state.index("(")+1:state.index(",")])
        col_idx = int(state[state.index(",")+1:state.index(")")])

        return row_idx, col_idx

    def plot(self, state: State = None, ax=None)->Dict[str, Any]:
        """

        :param ax: Axes to plot things on if one doesn't already exist.
        :return:
        """
        # Input Processing
        if ax is None:
            fig = plt.figure()
            ax = fig.subplots(1, 1, 1)
        if state is not None:
            assert state in self.S, f" State {state} is not in state space!"

        # Constants
        square_sl = 1.0
        circle_radius = square_sl/4.0

        # Plot the grid of state spaces
        self.plot_environment(ax, square_sl=square_sl)

        # Place Current State
        if state is not None:
            row_idx, col_idx = self.state_name_to_coordinates(state)
            curr_state_circle = Circle((col_idx, row_idx), circle_radius, color="red")
            robot_patch = ax.add_patch(curr_state_circle)

        # Set Axis
        ax.set_xlim([-square_sl, self.n_cols * square_sl])
        ax.set_ylim([- square_sl, self.n_rows * square_sl])

        return {"robot": robot_patch}

    def plot_environment(self, ax: plt.Axes, square_sl: float = 1.0):
        # Constants

        # Algorithm
        for row_idx in range(self.n_rows):
            for col_idx in range(self.n_cols):
                state_name = f"s_({col_idx},{row_idx})"

                in_windy_region = (self.windy_region_y_lb <= row_idx) and (row_idx <= self.windy_region_y_ub)
                in_lava_region = (col_idx == 0) or (col_idx == self.n_cols - 1)

                color = "blue" if in_windy_region else "black"
                color = "red" if in_lava_region else color
                color = "green" if ("Surveil1" in self.L(state_name)) or ("Surveil2" in self.L(state_name)) else color
                color = "yellow" if state_name in self.I else color

                s_i_square = Rectangle(
                    (col_idx * square_sl - square_sl/2., row_idx*square_sl - square_sl/2.),
                    square_sl, square_sl,
                    fill=True,
                    alpha=0.5,
                    color=color,
                )
                ax.add_patch(s_i_square)

    def plot_trajectory(self, traj: FiniteTrajectory, ax=None):
        """
        plot_trajectory
        Description:
            Plots the trajectory provided in traj.
        :param traj:
        :param ax:
        :return: Returns an axis object/figure where the
        """
        # Input Processing
        if ax is None:
            fig = plt.figure()
            ax = fig.subplots(1, 1, 1)

        # Constants
        square_sl = 1.0
        circle_radius = square_sl / 4.0

        # Plot the grid of state spaces
        self.plot_environment(ax, square_sl=square_sl)

        # Plot trajectory
        for k in range(len(traj)):
            s_k = traj.s(k)
            row_idx, col_idx = self.state_name_to_coordinates(s_k)
            curr_state_circle = Circle((col_idx, row_idx), circle_radius, color="red")
            ax.add_patch(curr_state_circle)

        # Set Axis
        ax.set_xlim([-square_sl, self.n_cols * square_sl])
        ax.set_ylim([- square_sl, self.n_rows * square_sl])

    def save_animated_trajectory(self, traj: FiniteTrajectory, filename: str, ax=None, fps: int = 2):
        """
        save_animated_trajectory
        Description:
            Creates a gif or video of the target trajectory.
        :param traj:
        :param filename: Filename to save the animation to.
        :param ax:
        :return:
        """
        # Constants
        num_frames = len(traj)

        # Create a figure and an axis.
        fig = plt.figure()
        ax = fig.add_subplot(111)

        # Plot the initial state.
        plot_objects = self.plot(state=traj.s(0), ax=ax)

        # Create a function to update the plot.
        def update(frame_index):
            # Update robot position
            plot_objects["robot"].center = np.flip(self.state_name_to_coordinates(traj.s(frame_index)))

        # Construct the animation, using the update function as the animation
        # director.
        animation = manimation.FuncAnimation(
            fig, update,
            np.arange(0, num_frames - 1),
        )

        animation.save(filename=filename, fps=fps)

def get_noisy_sadra_system():
    """Gets sadra system."""

    return SadraSystem()




def add_perturbed_transitions_for_mode(
    ts: ParametricTransitionSystem,
    theta: Parameter,
    state_coords: Tuple[int],
    n_rows: int = 10, n_cols: int = 15,
):
    """
    add_adjacent_transitions_for_mode
    Description:

    :param ts:
    :param theta: String representing the current parameter.
    :param s: tuple containing the row_index and col_index
    :return: Nothing. Transition systems hould be modified to
    """
    # Constants

    # Create string for state
    s_i = f"s_({state_coords[0]},{state_coords[1]})"

    # Add Transitions
    s_i_up = f"s_({max(state_coords[0]-1, 0)},{max(0,state_coords[1]-2)})"
    ts.add_transition(s_i, "up", theta, s_i_up)

    s_i_down = f"s_({min(state_coords[0]+1, n_rows)},{max(0, state_coords[1]-2)})"
    ts.add_transition(s_i, "down", theta, s_i_down)

    s_i_left = f"s_({state_coords[0]},{max(state_coords[1]-3, 0)})"
    ts.add_transition(s_i, "left", theta, s_i_left)

    s_i_right = f"s_({state_coords[0]},{max(state_coords[1]-1, 0)})"
    ts.add_transition(s_i, "right", theta, s_i_right)

# x_i = 's_(8,13)'

# sadra = get_sadra_system()
# transitions = []

# for transition in sadra.transitions:
#     if sadra.Y[transition[0]] == x_i:
#         transitions.append(transition)
# for transition in transitions: 
#     if sadra.Act[transition[1]] == 'up': print(transition)