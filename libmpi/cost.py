import os
import subprocess
import re
from libmpi.path import MAKEFILE_PATH

def execute_binary(olevel, simd, n1, n2, n3, num_threads, num_reps, n1_size, n2_size, n3_size):
    filename = "iso3dfd_dev13_cpu_" + olevel + "_" + simd + ".exe"
    cmd = "bin/" + filename + \
        " " + n1 + " " + n2 + " " + n3 + \
        " " + num_threads + " " + num_reps + \
        " " + n1_size + " " + n2_size + " " + n3_size
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    os.chdir("./..")
    return res

def execute_makefile(olevel="-O3", simd="avx2"):
    os.chdir(MAKEFILE_PATH)
    
    # Do not compile again if exe already exists
    if os.path.exists("bin/iso3dfd_dev13_cpu_" + olevel + "_" + simd + ".exe"):
        return
    
    cmd = "make Olevel=" + olevel + \
          " simd=" + simd + \
          " last > dump.txt"
    os.system(cmd)

def find_cost(res):
    pattern_gflops = "(\d+.\d+) GFlops"
    pattern_time= "(\d+.\d+) sec"
    find_gflops = re.search(pattern_gflops, str(res))
    find_time = re.search(pattern_time, str(res))
    gflops = float(find_gflops.group()[:-7]) if find_gflops else 0.0
    time = float(find_time.group()[:-4]) if find_time else 0.0
    return (gflops, time)

def cost_function(olevel, simd, n1, n2, n3, num_threads, num_reps, n1_size, n2_size, n3_size):
    execute_makefile(olevel, simd)
    res = execute_binary(olevel, simd, n1, n2, n3, num_threads, num_reps, n1_size, n2_size, n3_size)
    return find_cost(res)

