import os
import subprocess
import re

def execute_binary(simd, n1, n2, n3, num_threads, num_reps, n1_size, n2_size, n3_size):
    filename = "iso3dfd_dev13_cpu_" + simd + ".exe"
    cmd = "bin/" + filename + \
        " " + n1 + " " + n2 + " " + n3 + \
        " " + num_threads + " " + num_reps + \
        " " + n1_size + " " + n2_size + " " + n3_size
    print("The compilation will be done through:")
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

def find_cost(res) -> float:
    pattern = "(\d+.\d+) GFlops"
    find = re.search(pattern, str(res))
    if find:
        print("Result --->", float(find.group()[:-7]))
    return float(find.group()[:-7]) if find else 0.0

def cost_function(o_level, simd, n1, n2, n3, num_threads, num_reps, n1_size, n2_size, n3_size) -> float:
    execute_makefile(o_level, simd)
    res = execute_binary(simd, n1, n2, n3, num_threads, num_reps, n1_size, n2_size, n3_size)
    return find_cost(res)





