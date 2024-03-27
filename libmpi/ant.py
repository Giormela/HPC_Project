from libmpi.param import *
from libmpi.cost import *

class Ant:
    def __init__(self):
        self.pheromon_mult = 1.0
        self.solution = {}
        self.points = 0.0

    def get_param_solution(self, param) -> str:
        return self.solution[param] if param in self.solution else PARAMS_DICT[param].default
    
    def get_solution(self):
        res = {}
        for param in PARAMS_DICT:
            res[param] = self.get_param_solution(param)
        return res
    
    def export_solution(self):
        # Treat differently olevel and simd
        olevel = PARAMS_DICT["olevel"].get_index_from_value(self.get_param_solution("olevel"))
        simd = PARAMS_DICT["simd"].get_index_from_value(self.get_param_solution("simd"))
        
        res = {tuple[0]: self.get_param_solution(tuple[0]) for tuple in PARAMS_DICT.items()}
        res["gflops"] = self.points
        res["olevel"] = olevel
        res["simd"] = simd
        return res

    def rank_solution(self, size):
        olevel = self.get_param_solution("olevel")
        simd = self.get_param_solution("simd")
        num_threads = self.get_param_solution("num_threads")
        n1_size = self.get_param_solution("n1_size")
        n2_size = self.get_param_solution("n2_size")
        n3_size = self.get_param_solution("n3_size")

        self.points = cost_function(olevel, simd, size, size, size, num_threads, "100", n1_size, n2_size, n3_size)

    
    def add_solution(self, param: Param, index: int):
        self.solution[param.get_name()] = param.get_value_by_index(index)