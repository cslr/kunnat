# Kunnat

QUANTUM COMPUTING:

D-Wave's Quantum Optimization Using Municipalities Statistics and Average Income (DQM model)

Attempt to use Municipalities data to learn which budgets give highest income from the population (through taxation).

Code for quantum computing optimization is in **etl_data.py**.

Theory is described in **quantum_optimization.pdf**.

RESULTS:

Nothing surprising. Biggest values in each variable (divided by the number of residents) result to highest income per resident. Data from Finnish Statistics Center (small dataset).


NORMAL COMPUTING:

Code to fit linear model to dy(t+1)/dt = A*t(t) + f(t) optimal control problem is in **optimal_control.py**. It also generates graphs showing results.
