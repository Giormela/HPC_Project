import os
import sys
import subprocess
import re

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
    print(find.group())

#-----------------------------------------------------------------
# Main code
#-----------------------------------------------------------------
#print("Deployment using OS module")
#print("")
#print("")

#(o_level, simd, n1, n2, n3, num_threads, num_reps, n1_size, n2_size, n3_size) = cmdLineParsing()

#execute_makefile(o_level, simd)

#res = execute_binary(simd, n1, n2, n3, num_threads, num_reps, n1_size, n2_size, n3_size)

#collect_result(res)



