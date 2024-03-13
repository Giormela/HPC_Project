from typing import List
from enum import Enum
from lib.ant import *

class RedistributionStrategy(Enum):
    Linear = 1
    Quadratic = 2
    Relu = 3


def set_ants_mult(ants: List[Ant], strategy=RedistributionStrategy.Linear):
    fun = None

    match strategy:
        case RedistributionStrategy.Linear:
            fun = linear_redistribution
        case RedistributionStrategy.Quadratic:
            fun = quadatic_redistribution
        case RedistributionStrategy.Relu:
            fun = relu_redistribution

    fun(ants)

def linear_redistribution(ants: List[Ant]):
    top = 2.0
    step = top / len(ants)

    coeff = top
    for ant in ants:
        ant.pheromon = abs(coeff)
        coeff -= step

# y = a / x
def quadatic_redistribution(ants: List[Ant]):
    top = 2.0

    for i in range(len(ants)):
        ants[i] = top / (i+1)^2


def relu_redistribution(ants: List[Ant]):
    return