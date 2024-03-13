from lib.ant import * 
from lib.redistribution import *
from lib.exporter import dump_state
import random

PARAMS_TO_EXPLORE = ["olevel", "simd", "num_threads", "n1_size", "n2_size", "n3_size"]

#----------------------------------------------------------------
# param - Parameter whose node model the choise
# children - List of children nodes (one for each option of the choise)
# probs - List of probability to get each child
# pheromons - List of pheromon laid down to each child
#----------------------------------------------------------------
class Node:
    def __init__(self, param: Param = None):
        self.param = param
        self.children = []
        self.probs = []
        self.pheromons = []
        self.ants_cross = []
    
    def explored_by_ant(self, ant: Ant):
        self.ants_cross.append(ant)
        if not self.param:
            return
        index = self.choose_child()
        ant.add_solution(self.param, index)
        self.children[index].explored_by_ant(ant)

    def update_pheromon(self, rho, delta):
        # Part of the pheromon evaporate for every arc
        self.pheromons = [pheromon * (1.0 - rho) for pheromon in self.pheromons] 
        # Each arc receives a quantity of pheromon
        for i in range(self.param.domain_dim):
            self.pheromons[i] += sum(ant.pheromon_mult * delta for ant in self.children[i].ants_cross)
        
    def update_probability(self):
        total = sum(self.pheromons)
        self.probs = [pheromon / total  for pheromon in self.pheromons]


    def choose_child(self) -> int:
        return random.choices(range(self.param.domain_dim), weights=self.probs, k=1)[0]

    def clear(self):
        self.ants_cross = []

#----------------------------------------------------------------
# N - Nb of ants
# ants - List of ants
# rho - Percentage of pheromon that will evaporate at each iteration
# delta - Quantity of pheromon released by each ant (times the its multiplier)
# root - Root of the tree which simulate the colony
#----------------------------------------------------------------
class Colony:
    def create_nodes(params_to_explore) -> Node:  
        if not params_to_explore: 
            return Node()   
        param = PARAMS_DICT[params_to_explore.pop(0)] 

        node = Node(param)
        node.children = [Colony.create_nodes(params_to_explore.copy()) for i in range(param.domain_dim)] 
        node.probs = [1.0/len(node.children) for i in range(param.domain_dim)]
        node.pheromons = [1.0 for i in range(param.domain_dim)]
        return node

    def __init__(self, N=100, rho=0.1, delta=0.05, params_to_explore=PARAMS_TO_EXPLORE): 
        self.N = N
        self.rho = rho
        self.delta = delta
        self.ants = [Ant() for i in range(N)]
        self.root = Colony.create_nodes(params_to_explore)

    def update_nodes(self, node: Node=None):
        # Initali condition
        if not node:
            node = self.root

        # Exit condition: we have reaced a leaf
        if not node.param:
            return
        
        # Update pheromon of every arc coming out from the node
        node.update_pheromon(self.rho, self.delta)
        # Update probability of every arc coming out from the node according to their pheromon level
        node.update_probability()
        # Reset node for next iteration
        node.clear()
        # Recursion into each children 
        for child in node.children:
            self.update_nodes(child)

    def rank_ants(self):
        # Evaluate the cost of each ant solution
        for ant in self.ants:
            ant.rank_solution()
        # Sort ants according to Gflops
        ranked = sorted(self.ants, key=lambda x: x.points, reverse=True)
        # Set ants' multiplier according to the rank position
        set_ants_mult(self.ants, RedistributionStrategy.Linear) 
    

    def run(self):
        for ant in self.ants:
            self.root.explored_by_ant(ant)

    def simulate(self, iter):
        for i in range(iter):
            # Let each ant explore the tree
            self.run()
            # Test solutions and define multiplier of each ant according to the rank achieved
            self.rank_ants()
            # Update pheromon and probability of each node
            self.update_nodes()
            # Dump solution for visualization
            dump_state(i, [ant.get_solution() for ant in self.ants])

    def print(self, list=None):
        if not list:
            list = [self.root]
        new_list = []
        for node in list:
            print(node.pheromons, node.probs, end="\t|\t")
            new_list.extend(node.children)
        print("\n")
        if new_list:
            self.print(new_list)

     