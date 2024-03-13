from libmpi.ant import * 
import random

PARAMS_TO_EXPLORE = ["olevel", "simd", "num_threads", "n1_size", "n2_size", "n3_size"]

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
        index = self.chose_child()
        ant.add_solution(self.param, index)
        self.children[index].explored_by_ant(ant)

    def update_pheromon(self, rho, delta):
        # Part of the pheromon evaporate for every arc
        self.pheromons = [pheromon * (1.0 - rho) for pheromon in self.pheromons] 
        # Each arc receives a quantity of pheromon
        for i in range(self.param.domain_dim):
            self.pheromons[i] += sum(ant.pheromon * delta for ant in self.children[i].ants_cross)

    def update_probability(self):
        for i in range(self.param.domain_dim):
            self.probs[i] = self.pheromons[i] / sum(self.pheromons)


    def chose_child(self) -> int:
        return random.choices(range(self.param.domain_dim), weights=self.probs, k=1)[0]

    def clear(self):
        self.ants_cross = []

  
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
        ranked = sorted(self.ants, key=lambda x: x.points, reverse=True)

        coeff = 2.0
        step = 2.0 / self.N
        for ant in ranked:
            ant.pheromon = abs(coeff)
            coeff -= step
        
        return ranked[0].solution
        
    def get_solutions(self):
        return [ant.solution for ant in self.ants]
    
    def run(self):
        for ant in self.ants:
            self.root.explored_by_ant(ant)
        return self.get_solutions()

    def simulate(self, iter):
        for i in range(iter):
            # Let each ant explore the tree
            self.run()
            # Test solutions and define multiplier of each ant according to the rank achieved
            self.rank_ants()
            # Update pheromon and probability of each node
            self.update_nodes()


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

     