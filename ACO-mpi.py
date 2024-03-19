import sys
from mpi4py import MPI
from libmpi.cost import cost_function
from libmpi.colony import Colony
from libmpi.redistribution import RedistributionStrategy
from libmpi.path import get_user_id_from_console, set_user_id


if len(sys.argv) > 1:
  ASKING_USER_ID = True

ITER = 50

comm = MPI.COMM_WORLD
Me = comm.Get_rank()
size = comm.Get_size()
print("Me: ", Me, "Size: ", size)





if Me == 0:
  # Getting user id and sharing it to all the other processes
  if ASKING_USER_ID:
    user_id = get_user_id_from_console()
    set_user_id(user_id)
    for i in range(1, size):
      comm.bsend(user_id, dest=i)  

  colony = Colony(rho=0.1, delta=0.1, N=20, redistribution_strategy=RedistributionStrategy.Quadratic)
  # The list of words to distribute - ensure it's the same length as the number of processes
  for i in range(ITER):
    solutions = colony.run()

    q = len(solutions) // size
    r = len(solutions) % size
    # Send each word to each process, including itself
    j = q + 1 if 0 < r else q
    for i in range(1, size):
      batch_size = q + 1 if i < r else q
      comm.bsend(solutions[j:j+batch_size], dest=i)
      j += batch_size

    # Process 0's batch
    results = []
    batch = solutions[:q + 1 if 0 < r else q]
    for i, solution in batch:
      results.append((i, cost_function(solution["olevel"], solution["simd"], "256", "256", "256", solution["num_threads"], "100", solution["n1_size"], solution["n2_size"], solution["n3_size"])))
    
    # Collect the modified word from each process
    for i in range(1, size):
      results_i = comm.recv(source=i)
      results += results_i
    
    # Update the pheromons
    colony.set_results(results)
    colony.rank_ants()
    colony.update_nodes()
else:
  # Setting user id from getting it from master 
  if ASKING_USER_ID:
    user_id = comm.recv(source=0)
    set_user_id(user_id)  

  # Other processes receive their word, add a trailing space, and send it back
  for i in range(ITER):
    batch = comm.recv(source=0)
    results = []
    for i, solution in batch:
      results.append((i, cost_function(solution["olevel"], solution["simd"], "256", "256", "256", solution["num_threads"], "100", solution["n1_size"], solution["n2_size"], solution["n3_size"])))
    comm.ssend(results, dest=0)