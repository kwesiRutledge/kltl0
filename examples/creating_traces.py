from kltl.systems.ts import get_beverage_vending_machine, create_random_trajectory_with_N_actions
from kltl.grammar.ltl import Eventually

# Create Beverage Vending Machine
ts = get_beverage_vending_machine()

traj = create_random_trajectory_with_N_actions(ts, 10)
print("Created the random trajectory with initial condition:")
print(traj.s(0))

random_trace = traj.trace()
print("Computed trace of the random trajectory!")
print(random_trace)

# Check the random trajectory on a formula.
random_ap = ts.AP[1]
formula = Eventually(random_ap)
print("Checking the random trajectory on the formula:")
print(formula)
print(random_trace.satisfies(formula))
