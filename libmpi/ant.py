from libmpi.param import *
from libmpi.cost import *

class Ant:
    def __init__(self):
        self.pheromon_mult = 1.0
        self.solution = {}
        self.points = 0.0

    def get_param_solution(self, param) -> str:
        sol = self.solution[param] if param in self.solution else PARAMS_DICT[param].default
        return str(sol)
    
    def get_solution(self):
        res = {}
        for param in PARAMS_DICT:
            res[param] = self.get_param_solution(param)
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