
from mpi4py import MPI
from libmpi.cost import cost_function
from libmpi.colony import Colony


comm = MPI.COMM_WORLD
Me = comm.Get_rank()
size = comm.Get_size()

iter = 10

if Me == 0:
  colonny = Colony(rho=0.1, delta=0.1, N=8)
  # The list of words to distribute - ensure it's the same length as the number of processes
  for i in range(iter):
    solutions = colonny.run()

    q = len(solutions) // size
    r = len(solutions) % size
    # Send each word to each process, including itself
    j = q + 1 if 0 < r else q
    for i in range(1, size):
      batch_size = q + 1 if i < r else q
      comm.send(solutions[j:j+batch_size], dest=i)
      j += batch_size

    # Process 0's batch
    results = []
    batch = solutions[:q + 1 if 0 < r else q]
    for solution in batch:
      results.append(cost_function(solution["olevel"], solution["simd"], "256", "256", "256", solution["num_threads"], "100", solution["n1_size"], solution["n2_size"], solution["n3_size"]))
    
    # Collect the modified word from each process
    for i in range(1, size):
      results_i = comm.recv(source=i)
      results += results_i
    
    # Append the modified words together and print
    print(results)
else:
  # Other processes receive their word, add a trailing space, and send it back
  for i in range(iter):
    batch = comm.recv(source=0)
    results = []
    for solution in batch:
      results.append(cost_function(solution["olevel"], solution["simd"], "256", "256", "256", solution["num_threads"], "100", solution["n1_size"], solution["n2_size"], solution["n3_size"]))
    comm.send(results, dest=0)