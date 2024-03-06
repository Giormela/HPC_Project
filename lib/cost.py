import os
import subprocess
import re

def execute_binary(olevel, simd, n1, n2, n3, num_threads, num_reps, n1_size, n2_size, n3_size):
    filename = "iso3dfd_dev13_cpu_" + olevel + "_" + simd + ".exe"
    cmd = "bin/" + filename + \
        " " + n1 + " " + n2 + " " + n3 + \
        " " + num_threads + " " + num_reps + \
        " " + n1_size + " " + n2_size + " " + n3_size
    print("The execution will be done through:")
    print("\t"+cmd)
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    return res

def execute_makefile(o_level="-O3", simd="avx2"):
    os.chdir("/usr/users/st76i/st76i_1/iso3dfd-st7")
    cmd = "make Olevel=" + o_level + \
          " simd=" + simd + \
          " last > dump.txt"
    print("The compilation will be done through:")
    print("\t"+cmd)
    os.system(cmd)

def find_cost(res) -> float:
    pattern = "(\d+.\d+) GFlops"
    find = re.search(pattern, str(res))
    if find:
        print("Result --->", float(find.group()[:-7]))
        print(" ")
    return float(find.group()[:-7]) if find else 0.0

def cost_function(o_level, simd, n1, n2, n3, num_threads, num_reps, n1_size, n2_size, n3_size) -> float:
    execute_makefile(o_level, simd)
    res = execute_binary(o_level, simd, n1, n2, n3, num_threads, num_reps, n1_size, n2_size, n3_size)
    return find_cost(res)

