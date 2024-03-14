from lib.colony import *
from lib.path import *

colony = Colony(N=20, rho=0.1, delta=0.1)

colony.simulate(iter=10)

