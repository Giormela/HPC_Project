import subprocess
from lib.colony import *
from lib.path import *

# Load modules on HPC system
subprocess.call(['bash', './run_subprocess.sh'])

colony = Colony(N=20, rho=0.1, delta=0.1)

colony.simulate(iter=10)

