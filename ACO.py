from lib.colony import *

colony = Colony(N=2, rho=0.1, delta=0.05, params_to_explore=["olevel"])

colony.simulate(iter=2)


    