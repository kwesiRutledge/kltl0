from kltl.systems import get_beverage_vending_machine, create_random_trajectory_with_N_actions

# Create Beverage Vending Machine
ts = get_beverage_vending_machine()

traj = create_random_trajectory_with_N_actions(ts, 10)

print(traj.s(0))

random_trace = [ ts.L( traj.s(k) ) for k in range(len(traj))]

print(random_trace)