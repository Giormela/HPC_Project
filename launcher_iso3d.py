

import argparse
import os
import subprocess
import sys
import uuid

# TODO seed
MatSizeDefault = 4096

def runSub(matSize,strategy,Olevel,vectorExtension):
    filename = uuid.uuid4().hex
    os.system("srun hostname | sort -u > " + filename)
    file = open(filename,"r")
    liste = file.readlines()
    nbNodes = len(liste)
    print("NbNodes: " + str(nbNodes) + ", Strategy: " + strategy)

    cmdMake = "make Olevel=-"+Olevel+" simd="+vectorExtension+" last"
    os.chdir("/usr/users/st76i/st76i_14/iso3dfd-st7/")
    os.system(cmdMake)
    if strategy == "socket":
        nbProcesses = 2*nbNodes
        cmd = "mpirun -np " + str(nbProcesses) + \
            " -map-by ppr:1:socket:PE=8 -rank-by socket " + \
            " python3 matprod.py " + " --s " + str(matSize) + " --nt 8 " + " --r "
        print("Executed command: " + cmd)
        print("---->")
        res = subprocess.run(cmd,shell=True,stdout=subprocess.PIPE) 
    if strategy == "core":
        nbProcesses = 16*nbNodes
        # filename .exe changes with compilation options
        cmd = "/usr/users/st76i/st76i_14/iso3dfd-st7/bin/iso3dfd_dev13_cpu_"+Olevel+"_"+vectorExtension+".exe 256 256 256 32 100 32 32 32"
        print("Executed command: " + cmd)
        print("---->")
        res = subprocess.run(cmd,shell=True,stdout=subprocess.PIPE)

    # - print MPI pgm output
    print(str(res.stdout,'utf-8'))

    # - remove the "allocated machines file" with a unique file name
    os.system("rm -f " + filename)

parser = argparse.ArgumentParser(
                    prog='launcher_iso3d',
                    description='run iso3d',
                    epilog='Welcome to Wolfgang Walters launcher')

parser.add_argument('matrix_size', default=MatSizeDefault, type=int)  # positional argument
parser.add_argument('-s', '--strategy',
    default="core",  # Instead of "None"
    choices=["socket","core"])      # option that takes a value
parser.add_argument('-l', '--Olevel',
    default="-O3",  # Instead of "None"
    choices=["-O1","-O2","-O3","-Ofast"])      # option that takes a value
parser.add_argument('-v', '--vector',
    default="avx5112",  # Instead of "None"
    choices=["sse","avx","avx2","avx512"])      # option that takes a value
args = parser.parse_args()

if args.matrix_size <= 0:
    sys.exit("Error: matrix size must be an integer greater than 0!")


runSub(args.matrix_size,args.strategy)