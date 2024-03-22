import argparse
import sys
from mpi4py import MPI
import numpy as np
from libmpi.cost import cost_function
from libmpi.colony import Colony
from libmpi.colony_min_max import ColonyMinMax
from libmpi.param import PARAMS_DICT
from libmpi.redistribution import RedistributionStrategy
from libmpi.path import set_user_id

comm = MPI.COMM_WORLD
Me = comm.Get_rank()
size = comm.Get_size()
print("Me: ", Me, "Size: ", size)

parser = argparse.ArgumentParser()
parser.add_argument('-u','--user',type=int, choices=range(1, 15))
parser.add_argument('-m','--method',type=int, choices=range(1, 4))
parser.add_argument('-i','--iter',type=int)
parser.add_argument('-n','--nbants',type=int)
parser.add_argument('-d','--delta',type=float)
parser.add_argument('-r','--rho',type=float)
parser.add_argument('-min',type=float)
parser.add_argument('-max',type=float)
args = parser.parse_args()
user_id = int(args.user) if args.user else 1
method = args.method if args.method else 1
ITER = args.iter if args.iter else 50
N = args.nbants if args.nbants else 20
delta = args.delta if args.delta else 0.1
rho = args.rho if args.rho else 0.1
min = args.min if args.min else 0.
max = args.max if args.max else float('inf')

def get_array_from_solution(solution):
  return np.array([PARAMS_DICT[param].get_index_from_value(solution[param]) for param in PARAMS_DICT])

def get_solution_from_array(array):
  return {param: PARAMS_DICT[param].get_value_by_index(array[i]) for i, param in enumerate(PARAMS_DICT)}

if Me == 0:
  # Choose the redistribution strategy
  if method == 1:
    redistribution_strategy = RedistributionStrategy.Linear
  elif method == 2:
    redistribution_strategy = RedistributionStrategy.Quadratic
  else:
    redistribution_strategy = RedistributionStrategy.Relu
  # Set and sharing user id 

  if min != 0 or max != np.inf:
    colony = ColonyMinMax(min=min, max=max, rho=rho, delta=delta, N=N, redistribution_strategy=redistribution_strategy)
  else:
    colony = Colony(rho=rho, delta=delta, N=N, redistribution_strategy=redistribution_strategy)

set_user_id(user_id)
for i in range(ITER):
  
  solutions = None
  if Me == 0:
    print(f"Iteration {i}")
    print("time accumulated", colony.execution_time)
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
    colony.rank_ants()
    colony.update_nodes()
    colony.export(i)