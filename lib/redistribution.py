from typing import List
from enum import Enum
from lib.ant import *

class RedistributionStrategy(Enum):
    Linear = 1
    Quadratic = 2
    Relu = 3
    Performance = 4


def set_ants_mult(ants: List[Ant], strategy=RedistributionStrategy.Linear):
    fun = None

    if strategy == RedistributionStrategy.Linear:
        fun = linear_redistribution
    elif strategy == RedistributionStrategy.Quadratic:
        fun = quadatic_redistribution
    elif strategy == RedistributionStrategy.Relu:
        fun = relu_redistribution
    elif strategy == RedistributionStrategy.Performance:
        fun = performance_redistribution
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
        
def performance_redistribution(ants: List[Ant]):
    for i in range(len(ants)):
        ants[i].pheromon_mult = 10*(ants[i].points/140)