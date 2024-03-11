#----------------------------------------------------------------
# name - Name of the parameter
# domain - List of possible values for the parameter
# default - Default choise (the parameter could be excluded by the creation of the tree)
# domain_dim - Cardinality of domain
#----------------------------------------------------------------
class Param:
    def __init__(self, name, domain, default):
        self.name = name
        self.domain = domain
        self.default = default
        self.domain_dim = len(domain)
    
    def get_value_by_index(self, index):
        return self.domain[index] if index < self.domain_dim else self.default
    
    def get_name(self):
        return self.name
    

PARAMS_DICT = {"olevel": Param("olevel", ["-O2", "-O3", "-Ofast"], "-O3"),
           "simd": Param("simd", ["sse", "avx", "avx2",  "avx512"], "avx2"),
           "num_threads": Param("num_threads", [i for i in range(1, 33)], 32),
           "n1_size": Param("n1_size", [32, 64, 128, 256], 32),
           "n2_size": Param("n2_size", [32, 64, 128, 256], 32),
           "n3_size": Param("n3_size", [32, 64, 128, 256], 32)}