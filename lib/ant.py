from lib.param import *
from lib.cost import cost_function

#----------------------------------------------------------------
# pheromono_mult - Coefficient responsible for pheromon deployment
# solution - Dictionary containing values found for each parameter
# points - Nb of Gflops obtained by the solution
#----------------------------------------------------------------
class Ant:
    def __init__(self):
        self.pheromon_mult = 1.0
        self.solution = {}
        self.points = 0.0

    def get_param_solution(self, param) -> str:
        return self.solution[param] if param in self.solution else PARAMS_DICT[param].default
    
    def export_solution(self):
        res = {tuple[0]: tuple[1].get_index_from_value(self.get_param_solution(tuple[0])) for tuple in PARAMS_DICT.items()}
        res["gflops"] = self.points
        return res

    def rank_solution(self):
        olevel = self.get_param_solution("olevel")
        simd = self.get_param_solution("simd")
        num_threads = self.get_param_solution("num_threads")
        n1_size = self.get_param_solution("n1_size")
        n2_size = self.get_param_solution("n2_size")
        n3_size = self.get_param_solution("n3_size")

        self.points = cost_function(olevel, simd, "256", "256", "256", num_threads, "100", n1_size, n2_size, n3_size)

    
    def add_solution(self, param: Param, index: int):
        self.solution[param.get_name()] = param.get_value_by_index(index)