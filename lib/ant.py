from param import *
from cost import *

class Ant:
    def __init__(self):
        self.pheromon = 1.0
        self.solution = {}
        self.points = 0.0

    def get_param_solution(self, param) -> str:
        value = self.solution[param] if param in self.solution else PARAMS_DICT[param].default
        return str(value)

    def test_solution(self):
        olevel = self.get_param_solution("olevel")
        simd = self.get_param_solution("simd")
        n = self.get_param_solution("n")
        num_threads = self.get_param_solution("num_threads")
        n_size = self.get_param_solution("n_size")

        execute_makefile(olevel, simd)
        execute_binary(simd, n, n, n, num_threads, str(100), n_size, n_size, n_size)
    
    def add_solution(self, param: Param, index: int):
        self.solution[param.get_name()] = param.get_value_by_index(index)