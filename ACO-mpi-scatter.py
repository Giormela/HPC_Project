import argparse
import subprocess
import sys
from mpi4py import MPI
import numpy as np
from libmpi.cost import cost_function
from libmpi.colony import Colony
from libmpi.colony_min_max import ColonyMinMax
from libmpi.param import PARAMS_DICT
from libmpi.redistribution import RedistributionStrategy
from libmpi.path import set_user_id

# Create MPI environment
comm = MPI.COMM_WORLD
Me = comm.Get_rank()
size = comm.Get_size()

# Define the shell arguments
parser = argparse.ArgumentParser(
                    prog='Iso3d Ant Optimization',
                    description='We run an ant colony to find the best paramters for an iso3d executions',
                    epilog='Good Luck :)')
parser.add_argument('-u','--user',type=int, help="user number in chome")
parser.add_argument('-m','--method',type=str, choices={'linear','relu','quadratic'},help="Pheromons distribution method")
parser.add_argument('-i','--iteration',type=int, help="number of iterations the ant colony algorithm")
parser.add_argument('-n','--numberOfAnt',type=int)
parser.add_argument('-d','--delta',type=float,help="base quantity of pheromons available for each ant")
parser.add_argument('-r','--rho',type=float,help="coefficient of evaporation of the pheromons")
parser.add_argument('-min',type=float,help="the minimum pheromon each edge can hold")
parser.add_argument('-max',type=float,help="the maximum pheromon each edge can hold")

#get the user if forgot to set
res = subprocess.run("whoami", shell=True, stdout=subprocess.PIPE)
res = str(res.stdout,'utf-8')

# Parse the shell arguments
args = parser.parse_args()
user_id = int(args.user) if args.user else int(res[6:])
method = args.method if args.method else 'linear'
ITER = args.iteration if args.iteration else 50
N = args.numberOfAnt if args.numberOfAnt else 20
delta = args.delta if args.delta else 0.1
rho = args.rho if args.rho else 0.1
min = args.min if args.min else 0.
max = args.max if args.max else float('inf')

# Set the user id for all processes
set_user_id(user_id)

# initialize the colony on the root process
if Me == 0:
  # Choose the redistribution strategy
  if method == 'linear':
    redistribution_strategy = RedistributionStrategy.Linear
  elif method == 'quadratic':
    redistribution_strategy = RedistributionStrategy.Quadratic
  elif method == 'relu':
    redistribution_strategy = RedistributionStrategy.Relu

  # Create the colony
  if min != 0 or max != np.inf:
    colony = ColonyMinMax(min=min, max=max, rho=rho, delta=delta, N=N, redistribution_strategy=redistribution_strategy)
  else:
    colony = Colony(rho=rho, delta=delta, N=N, redistribution_strategy=redistribution_strategy)

# Run the ACO algorithm
for i in range(ITER):
  
  solutions = None
  
  if Me == 0:
    print(f"------------------- Iteration {i} -------------------")
    solutions = colony.run()
    solutions = [[solutions[j] for j in range(i, len(solutions), size)] for i in range(size)]
  
  batch = comm.scatter(solutions, root=0)
  
  results = []
  
  for s, solution in batch:
    results.append((s, cost_function(solution["olevel"], solution["simd"], "256", "256", "256", solution["num_threads"], "100", solution["n1_size"], solution["n2_size"], solution["n3_size"])))
  
  results = comm.gather(results, root=0)
  
  if Me == 0:
    results = [item for sublist in results for item in sublist]
    colony.set_results(results)
    iter_best_solution, iter_best_result = colony.rank_ants()
    colony.update_nodes()
    colony.export(i)
    print(f"Iteration {i} best solution: {iter_best_solution} with {iter_best_result} Gflops")
    print()
    print(f"Overall best solution: {colony.best_solution} with {colony.best_result} Gflops")
    print()
    print(f"Number of cost function calls: {(i+1)*N}")
    print(f"Total Execution time: {round(colony.execution_time,2)} s")
    print(f"Total execution time x number of cores: {round(colony.execution_time*size*16, 2)}")
    print()