from lib.colony import Colony
from lib.colony import Node
from lib.colony import PARAMS_TO_EXPLORE
from lib.param import PARAMS_DICT

class NodeMinMax(Node):
    def __init__(ColonyMinMax, self):
        self.colony = ColonyMinMax
        super().__init__()


    def update_pheromon(self, rho, delta):
        min = self.colony.getMin()
        max = self.colony.getMax()
        # Part of the pheromon evaporate for every arc
        self.pheromons = [pheromon * (1.0 - rho) for pheromon in self.pheromons]
        if self.pheromons < min:
            self.pheromons = min
        if self.pheromons > max:
            self.pheromons = max

        # Each arc receives a quantity of pheromon
        for i in range(self.param.domain_dim):
            self.pheromons[i] += sum(ant.pheromon_mult * delta for ant in self.children[i].ants_cross)
     

class ColonyMinMax(Colony):
    def create_nodes(self, params_to_explore) -> Node:
        if not params_to_explore: 
            return NodeMinMax(self)   
        param = PARAMS_DICT[params_to_explore.pop(0)] 

        node = NodeMinMax(self, param)
        node.children = [Colony.create_nodes(params_to_explore.copy()) for i in range(param.domain_dim)] 
        node.probs = [1.0/len(node.children) for i in range(param.domain_dim)]
        node.pheromons = [1.0 for i in range(param.domain_dim)]
        return node
    
    def __init__(self, min, max, N=100, rho=0.1, delta=0.05):
        if(min>max):
            sys.exit("Error: max must be bigger or equal to min")
        else:
            self.min = min
            self.max = max
        super().__init__(N, rho, delta)
    
    def getMin(self):
        return self.min
    
    def getMax(self):
        return self.max

