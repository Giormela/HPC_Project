

import argparse
import os
import subprocess
import sys
import uuid

# TODO seed
MatSizeDefault = 4096

def runSub(matSize,strategy,Olevel,vectorExtension,x,y,z):
    subprocess.call(['bash', './run_subprocess.sh'])
    filename = uuid.uuid4().hex
    os.system("srun hostname | sort -u > " + filename)
    file = open(filename,"r")
    liste = file.readlines()
    nbNodes = len(liste)
    Olevel = "-"+Olevel
    print("NbNodes: " + str(nbNodes) + ", Strategy: " + strategy, "Olevel: "+Olevel+", vectorExtension: "+vectorExtension)
    cmdMake = "make Olevel="+Olevel+" simd="+vectorExtension+" last"
    os.chdir("/usr/users/st76i/st76i_14/iso3dfd-st7/")
    os.system(cmdMake)
    if strategy == "socket":
        nbProcesses = 2*nbNodes
        cmd = "mpirun -np " + str(nbProcesses) + \
            " -map-by ppr:1:socket:PE=8 -rank-by socket " + \
            "/usr/users/st76i/st76i_14/iso3dfd-st7/bin/iso3dfd_dev13_cpu_"+Olevel + \
            "_"+vectorExtension+".exe "+str(matSize)+" "+str(matSize)+" "+str(matSize) + \
                " 32 100 "+str(x)+" "+str(y)+" "+str(z)
        print("Executed command: " + cmd)
        print("---->")
        res = subprocess.run(cmd,shell=True,stdout=subprocess.PIPE) 
    if strategy == "core":
        nbProcesses = 16*nbNodes
        # filename .exe changes with compilation options
        cmd = "/usr/users/st76i/st76i_14/iso3dfd-st7/bin/iso3dfd_dev13_cpu_"+Olevel + \
            "_"+vectorExtension+".exe "+str(matSize)+" "+str(matSize)+" "+str(matSize) + \
                " 32 100 "+str(x)+" "+str(y)+" "+str(z)
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
    default="core",  
    choices=["socket","core"])      
parser.add_argument('-l', '--Olevel',
    default="O3", 
    choices=["O1","O2","O3","Ofast"])      
parser.add_argument('-v', '--vector',
    default="avx5112",  
    choices=["sse","avx","avx2","avx512"])
parser.add_argument('-x','--block_x',type=int) #  block size that each node has to calculate
parser.add_argument('-y','--block_y',type=int) #  block size that each node has to calculate
parser.add_argument('-z','--block_z',type=int) #  block size that each node has to calculate

args = parser.parse_args()

if 0 >= args.block_x > args.matrix_size or 0 >= args.block_y > args.matrix_size or 0 >= args.block_z > args.matrix_size:
    sys.exit("Error: block size must be an integer between 0 and matrix size!")


if args.matrix_size <= 0:
    sys.exit("Error: matrix size must be an integer greater than 0!")


runSub(args.matrix_size,args.strategy,args.Olevel,args.vector,args.block_x,args.block_y,args.block_z)