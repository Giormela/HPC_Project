from libmpi.ant import * 
from libmpi.redistribution import RedistributionStrategy, set_ants_mult
from libmpi.exporter import dump_state
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

    def __init__(self, 
                 N: int=100, 
                 rho: float=0.1, 
                 delta: float=0.05, 
                 redistribution_strategy: RedistributionStrategy=RedistributionStrategy.Linear, 
                 params_to_explore=PARAMS_TO_EXPLORE): 
        self.N = N
        self.rho = rho
        self.delta = delta
        self.redistribution_strategy = redistribution_strategy
        self.ants = [Ant() for i in range(N)]
        self.root = Colony.create_nodes(params_to_explore)
        self.best_solution = None
        self.best_result = 0.0

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
            if ant.points > self.best_result:
                self.best_result = ant.points
                self.best_solution = ant.get_solution()
                print(f"New best solution: {self.best_solution} with {self.best_result} Gflops")
        # Sort ants according to Gflops
        self.ants = sorted(self.ants, key=lambda x: x.points, reverse=True)
        # Set ants' multiplier according to the rank position
        set_ants_mult(self.ants, self.redistribution_strategy) 
    
        
    def get_solutions(self):
        return [(i, self.ants[i].get_solution()) for i in range(len(self.ants))]
    
    def set_results(self, results):
        for i, result in results:
            self.ants[i].points = result

    def export(self, nb_iter: int):
        dump_state(nb_iter, [ant.export_solution() for ant in self.ants])

    
    def run(self):
        for ant in self.ants:
            self.root.explored_by_ant(ant)
        return self.get_solutions()
     