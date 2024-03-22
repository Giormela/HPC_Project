import subprocess
from lib.colony import *
from lib.path import *
from lib.ColonyMinMax import *


# Load modules on HPC system
subprocess.call(['bash', './run_subprocess.sh'])

colony = ColonyMinMax(N=20, rho=0.1, delta=0.1, min=1, max=4)

colony.simulate(iter=5)