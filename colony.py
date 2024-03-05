from together import *
from lib import ant
from lib import param
import random

PARAMS_TO_EXPLORE = ["olevel", "simd", "n", "num_threads", "n_size"]

class Node:
    def __init__(self, param: Param):
        self.param = param
        self.options = []
        self.probs = []
        self.pheromons = []
        self.ants_cross = []
    
    def explore_R(self, ant: Ant):
        self.ants_cross.append(ant)
        index = random.choices(range(self.param.domain_dim), weights=self.probs, k=1)[0]
        ant.add_solution(self.param, index)
        if not self.options[index]:
            return
        self.options[index].explore_R(ant)

    
    def clear(self):
        self.ants_cross = []
  
class Colony:
    def create_colony_R(domains_to_explore) -> Node:
        if not domains_to_explore:
            return None
        
        layer = PARAMS_DICT[domains_to_explore.pop(0)]

        node = Node(layer)
        node.options = [Colony.create_colony_R(domains_to_explore.copy()) for i in range(len(layer.domain))]
        node.probs = [1.0/len(node.options) for i in range(len(node.options))]
        node.pheromons = [1.0 for i in range(len(node.options))]
        return node

    def __init__(self, N=100, rho=0.1, delta=0.05): 
        self.N = N
        self.rho = rho
        self.delta = delta
        self.ants = [Ant() for i in range(N)]
        self.root = Colony.create_colony_R(PARAMS_TO_EXPLORE)

    def update_pheromon(self, node=None):
        if not node:
            node = self.root
        node.pheromons *= float(1.0 - self.rho)
        node.pheromons += sum(ant.pheromon * self.delta for ant in node.ants_cross)
        for option in node.options:
            self.update_pheromon(option)

    def update_probability(self, node=None):
        if not node:
            node = self.root
        
        for i in range(len(node.probs)):
            node.probs[i] = node.pheromons[i] / sum(node.pheromons)

        for option in node.options:
            self.update_probability(option)

    def update_ants(self):
        for ant in self.ants:
            ant.test_solution()

    
    def run(self):
        for ant in self.ants:
            self.root.explore_R(ant)

    def simulate(self, iter):
        for i in range(iter):
            self.run()
            #self.update_pheromon()
            self.update_ants()
            self.update_probability()

     