import os
import argparse

parser = argparse.ArgumentParser(
                    prog='Iso3d Ant Optimization',
                    description='We run an ant colony to find the best paramters for an iso3d executions',
                    epilog='Good Luck :)')
parser.add_argument('-np','--numberOfProc',type=int, choices={1,2,3,4,5,6,7,8}, help="number of processes created by MPI")
parser.add_argument('-m','--method',type=str, choices={'linear','relu','hyperbolic','performance'},help="pheromons distribution method linear, relu or quadratic")
parser.add_argument('-i','--iteration',type=int, help="number of iterations the ant colony algorithm")
parser.add_argument('-n','--numberOfAnt',type=int)
parser.add_argument('-s','--size',type=int, choices={256, 512}, help="Problem size")
parser.add_argument('-d','--delta',type=float,help="base quantity of pheromons available for each ant")
parser.add_argument('-r','--rho',type=float,help="coefficient of evaporation of the pheromons")
parser.add_argument('--min',type=float,help="the minimum pheromon each edge can hold")
parser.add_argument('--max',type=float,help="the maximum pheromon each edge can hold")
parser.add_argument('--cachegrind', nargs='?', const=True, default=False, help="adds the test of valgrind with cachegrind for the best result at the end")

args = parser.parse_args()
np = args.numberOfProc if args.numberOfProc else 1
method = args.method if args.method else 'linear'
iter = args.iteration if args.iteration else 50
n = args.numberOfAnt if args.numberOfAnt else 20
delta = args.delta if args.delta else 0.1
rho = args.rho if args.rho else 0.1
min = args.min if args.min else 0.
max = args.max if args.max else float('inf')
pb_size = args.size if args.size else 256
cachegrid_flag = ""
if args.cachegrind:
    cachegrid_flag = "--cachegrind"


cmd = "/usr/bin/mpirun -np "+str(np)+" python3 ACO-mpi-scatter.py --method "+method+" --iter "+str(iter)+" --numberOfAnt "+str(n)+" --delta "+str(delta)+" --rho "+str(rho)+" --min "+str(min)+" --max "+str(max)+" "+cachegrid_flag

os.system("./load_module.sh")
os.system(cmd)