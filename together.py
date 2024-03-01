##---------------------------------------------------------------
# S. Vialle
# February 2023
#---------------------------------------------------------------
#---------------------------------------------------------------

import os
import uuid
import argparse
import sys
import subprocess
import re

DefaultSize = 4096

#----------------------------------------------------------------
# Deployment function: launch a MPI4PY pgm on a set of cluster nodes
# + autocompute the number of allocated nodes
#----------------------------------------------------------------
def deployOS(matSide,strategy):
   # - Generates the "allocated machines file" with a unique file name
   filename = uuid.uuid4().hex
   print(filename)
   os.system("srun hostname | sort -u > " + filename)
   # - Automatic counting of the number of allocated nodes
   file = open(filename,"r")
   lines = file.readlines()
   nbNodes = len(lines)
   # - Deployment of the application on all the allocated nodes 
   #    according to the deployment rules and strategy
   print("NbNodes: " + str(nbNodes) + ", Strategy: " + strategy) 
   # - "socket" deployment strategy on Kyle
   if strategy == "socket":
      nbProcesses = 2*nbNodes
      cmd = "/usr/bin/mpirun -np " + str(nbProcesses) + \
            " -map-by ppr:1:socket:PE=8 -rank-by socket " + \
            " python3 matprod.py " + " --s " + str(matSide) + " --nt 8 " + " --r "
      print("Executed command: " + cmd)
      print("---->")
      os.system(cmd)

   # - "core" deployment strategy on Kyle
   if strategy == "core":
      nbProcesses = 16*nbNodes
      cmd = "/usr/bin/mpirun -np " + str(nbProcesses) + \
            " -map-by ppr:1:core:PE=1 -rank-by core " + \
            " python3 matprod.py " + " --s " + str(matSide) + " --nt 1 " + " --r "
      print("Executed command: " + cmd)
      print("---->")
      os.system(cmd)

   # - remove the "allocated machines file" with a unique file name
   os.system("rm -f " + filename)


#----------------------------------------------------------------
# Cmd line parsing
#----------------------------------------------------------------
def cmdLineParsing():
  if len(sys.argv) <= 10:
    sys.exit("Error: wrong number of arguments")

  return(sys.argv[1], sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7],sys.argv[8],sys.argv[9],sys.argv[10])

def execute_binary(simd, n1, n2, n3, num_threads, num_reps, n1_size, n2_size, n3_size):
  filename = "iso3dfd_dev13_cpu_" + simd + ".exe"
  cmd = "bin/" + filename + \
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
  #os.system(cmd)

def execute_makefile(o_level="-O3", simd="avx2"):
  os.chdir("..")
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
    print(find.group())

#-----------------------------------------------------------------
# Main code
#-----------------------------------------------------------------
print("Deployment using OS module")
print("")
print("")

(o_level, simd, n1, n2, n3, num_threads, num_reps, n1_size, n2_size, n3_size) = cmdLineParsing()

execute_makefile(o_level, simd)

res = execute_binary(simd, n1, n2, n3, num_threads, num_reps, n1_size, n2_size, n3_size)

collect_result(res)



