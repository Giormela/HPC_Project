from typing import List
from enum import Enum
from libmpi.ant import Ant

class RedistributionStrategy(Enum):
    Linear = 1
    Quadratic = 2
    Relu = 3


def set_ants_mult(ants: List[Ant], strategy=RedistributionStrategy.Linear):
    fun = None

    if strategy == RedistributionStrategy.Linear:
            fun = linear_redistribution
    elif strategy == RedistributionStrategy.Quadratic:
            fun = quadatic_redistribution
    elif strategy == RedistributionStrategy.Relu:
            fun = relu_redistribution

    fun(ants)

def linear_redistribution(ants: List[Ant]):
    top = 2.0
    step = top / len(ants)

    coeff = top
    for ant in ants:
        ant.pheromon_mult = abs(coeff)
        coeff -= step

# y = a / x
def quadatic_redistribution(ants: List[Ant]):
    top = 10.0

    for i in range(len(ants)):
        ants[i].pheromon_mult = top / ((i+1)**2)


def relu_redistribution(ants: List[Ant]):
    top = 2.0
    step = 2*top/(len(ants))

    for i in range(len(ants)):
        ants[i].pheromon_mult = max(top-step*i,0)