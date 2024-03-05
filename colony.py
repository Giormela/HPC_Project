import sys
from together import *
import random

class Ant:
    def __init__(self):
        self.pheromon = 1.0
        self.solution = {}
        self.points = 0.0

    def extract_param(self, param) -> str:
        if param in self.solution:
            return str(self.solution[param])
        else:
            str(DOMAINS[param].default)

    def test_solution(self):
        olevel = self.extract_param("olevel")
        simd = self.extract_param("simd")
        n = self.extract_param("n")
        num_threads = self.extract_param("num_threads")
        n_size = self.extract_param("n_size")

        execute_makefile(olevel, simd)
        execute_binary(simd, n, n, n, num_threads, str(100), n_size, n_size, n_size)

class Layer:
    def __init__(self, name, space_options, default):
        self.name = name
        self.space_options = space_options
        self.default = default

DOMAINS = {"olevel": Layer("olevel", ["-O2", "-O3", "-Ofast"], "-O3"),
           "simd": Layer("simd", ["avx2"], "avx2"),
           "n": Layer("n", [256, 512], 256),
           "num_threads": Layer("num_threads", [i for i in range(1, 33)], 32),
           "n_size": Layer("n_size", [16, 32, 64], 32),}

DOMAINS_TO_EXPLORE = ["olevel", "simd", "n", "num_threads", "n_size"]

class Node:
    def __init__(self, layer: Layer):
        self.layer = layer
        self.options = []
        self.probs = []
        self.pheromons = []
        self.ants_cross = []
    
    def explore_R(self, ant: Ant):
        self.ants_cross.append(ant)
        index = random.choices(range(len(self.options)), weights=self.probs, k=1)[0]
        ant.solution[self.layer.name] = self.layer.space_options[index]
        if not self.options[index]:
            return
        self.options[index].explore_R(ant)

    
    def clear(self):
        self.ants_cross = []
  
class Colony:
    def create_colony_R(domains_to_explore) -> Node:
        if not domains_to_explore:
            return None
        
        layer = DOMAINS[domains_to_explore.pop(0)]

        node = Node(layer)
        node.options = [Colony.create_colony_R(domains_to_explore.copy()) for i in range(len(layer.space_options))]
        node.probs = [1.0/len(node.options) for i in range(len(node.options))]
        node.pheromons = [1.0 for i in range(len(node.options))]
        return node

    def __init__(self, N=100, rho=0.1, delta=0.05): 
        self.N = N
        self.rho = rho
        self.delta = delta
        self.ants = [Ant() for i in range(N)]
        self.root = Colony.create_colony_R(DOMAINS_TO_EXPLORE)

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

     