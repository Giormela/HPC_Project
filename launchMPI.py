import os
import uuid
import argparse
import sys
import subprocess
import re

DefaultSize = 4096

def formulate_mpi_cmd(strategy):
    # - Generates the "allocated machines file" with a unique file name
    filename = uuid.uuid4().hex
    os.system("srun hostname | sort -u > " + filename)
    # - Automatic counting of the number of allocated nodes
    file = open(filename,"r")
    lines = file.readlines()
    nbNodes = len(lines)
    # - remove the "allocated machines file" with a unique file name
    os.system("rm -f " + filename)
    # - Deployment of the application on all the allocated nodes 
    #    according to the deployment rules and strategy
    print("NbNodes: " + str(nbNodes) + ", Strategy: " + strategy) 
    # - "socket" deployment strategy on Kyle
    if strategy == "socket":
        nbProcesses = 2*nbNodes
        return "/usr/bin/mpirun -np " + str(nbProcesses) + \
            " -map-by ppr:1:socket:PE=8 -rank-by socket "

    # - "core" deployment strategy on Kyle
    if strategy == "core":
        nbProcesses = 16*nbNodes
        return "/usr/bin/mpirun -np " + str(nbProcesses) + \
            " -map-by ppr:1:core:PE=1 -rank-by core"

def cmdLineParsing():
  if len(sys.argv) <= 10:
    sys.exit("Error: wrong number of arguments")
  return(sys.argv[1], sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7],sys.argv[8],sys.argv[9],sys.argv[10])

def execute_binary(strategy, simd, n1, n2, n3, num_threads, num_reps, n1_size, n2_size, n3_size):
    os.chdir("/usr/users/st76i/st76i_1/iso3dfd-st7/bin")
    filename = "iso3dfd_dev13_cpu_" + simd + ".exe"
    cmd = formulate_mpi_cmd(strategy) + \
        " " + filename + \
        " " + n1 + " " + n2 + " " + n3 + \
        " " + num_threads + " " + num_reps + \
        " " + n1_size + " " + n2_size + " " + n3_size
    print("")
    print("")
    print("The execution will be done through:")
    print("\t"+cmd)
    print("")
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    return res

def execute_makefile(o_level="-O3", simd="avx2"):
  os.chdir("/usr/users/st76i/st76i_1/iso3dfd-st7")
  cmd = "make Olevel=" + o_level + \
        " simd=" + simd + \
        " last"
  print("The compilation will be done through:")
  print("\t"+cmd)
  print("")
  os.system(cmd)

def collect_result(res):
  pattern = "(\d+.\d+) GFlops"
  find = re.search(pattern, str(res))
  if find:
    print("Result --->",find.group())



#-----------------------------------------------------------------
# Main code
#-----------------------------------------------------------------
(o_level, simd, n1, n2, n3, num_threads, num_reps, n1_size, n2_size, n3_size) = cmdLineParsing()

execute_makefile(o_level, simd)
res = execute_binary("core", simd, n1, n2, n3, num_threads, num_reps, n1_size, n2_size, n3_size)

collect_result(res)