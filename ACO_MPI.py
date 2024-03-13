from mpi4py import MPI

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    # The list of words to distribute - ensure it's the same length as the number of processes
    words = ['Hello', 'world', 'from', 'MPI', 'for', 'Python']
    # Check if there are enough words for all processes
    if len(words) != size:
        raise ValueError("The number of words must match the number of processes.")
    
    # Send each word to each process, including itself
    for i in range(1, size):
        comm.send(words[i], dest=i)
    
    # Process 0 also adds a trailing space to its word
    modified_words = [words[0] + " "]
    
    # Collect the modified word from each process
    for i in range(1, size):
        modified_word = comm.recv(source=i)
        modified_words.append(modified_word)
    
    # Append the modified words together and print
    final_string = ''.join(modified_words)
    print("Final string:", final_string)
else:
    # Other processes receive their word, add a trailing space, and send it back
    word = comm.recv(source=0)
    modified_word = word + " "
    comm.send(modified_word, dest=0)
