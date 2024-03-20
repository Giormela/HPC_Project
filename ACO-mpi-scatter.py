import argparse
import sys
from mpi4py import MPI
import numpy as np
from libmpi.cost import cost_function
from libmpi.colony import Colony
from libmpi.param import PARAMS_DICT
from libmpi.redistribution import RedistributionStrategy
from libmpi.path import set_user_id

comm = MPI.COMM_WORLD
Me = comm.Get_rank()
size = comm.Get_size()
print("Me: ", Me, "Size: ", size)

parser = argparse.ArgumentParser()
parser.add_argument('-u','--user',type=int, choices=range(1, 14))
parser.add_argument('-m','--method',type=int, choices=range(1, 4))
parser.add_argument('-i','--iter',type=int)
parser.add_argument('-n','--nbants',type=int)
parser.add_argument('-d','--delta',type=float)
parser.add_argument('-r','--rho',type=float)
args = parser.parse_args()
user_id = int(args.user) if args.user else 1
method = args.method if args.method else 1
ITER = args.iter if args.iter else 50
N = args.nbants if args.nbants else 20
delta = args.delta if args.delta else 0.1
rho = args.rho if args.rho else 0.1

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
  set_user_id(user_id)

  colony = Colony(rho, delta, N, redistribution_strategy)
else:
  # Setting user id 
  set_user_id(user_id)

for i in range(ITER):
  solutions = None
  # counts = None
  # displacements = None
  # batchSize = N // size + 1 if i < (N % size) else N // size + 1
  # batch = np.empty(batchSize, dtype=np.int*dict)
  if Me == 0:
    print(f"Iteration {i}")
    solutions = colony.run()
    # counts = [N // size + 1 if i < (N % size) else N // size for i in range(size)]
    # displacements = [sum(counts[:i]) for i in range(size)]
  batch = comm.scatter(solutions, root=0)
  print(f"Me: {Me} Batch: {batch}")
  results = []