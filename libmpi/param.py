#----------------------------------------------------------------
# name - Name of the parameter
# domain - List of possible values for the parameter
# default - Default choise (the parameter could be excluded by the creation of the tree)
# domain_dim - Cardinality of domain
#----------------------------------------------------------------
class Param:
    def __init__(self, name, domain, default, spread: bool =False):
        self.name = name
        self.domain = domain
        self.default = default
        self.spread = spread
        self.domain_dim = len(domain)
    
    def get_value_by_index(self, index):
        return self.domain[index] if index < self.domain_dim else self.default
    
    def get_index_from_value(self, value):
        return self.domain.index(value)
    
    def get_name(self):
        return self.name
    

PARAMS_DICT = {"olevel": Param(
                        name="olevel", 
                        domain=["-O3", "-Ofast"], 
                        default="-O3", 
                        spread=False),
           "simd": Param(
                        name="simd", 
                        domain=["sse", "avx", "avx2",  "avx512"], 
                        default="avx2", 
                        spread=False),
           "num_threads": Param(
                        name="num_threads", 
                        domain=[str(i) for i in range(16, 33)], 
                        default="32", 
                        spread=True),
           "n1_size": Param(
                        name="n1_size", 
                        domain=[str(16*i) for i in range(8,17)], 
                        default="32",
                        spread=True),
           "n2_size": Param(
                        name="n2_size", 
                        domain=[str(i) for i in range(1,33)], 
                        default="32", 
                        spread=True),
           "n3_size": Param(
                        name="n3_size",     
                        domain=[str(i) for i in range(1,33)], 
                        default="32", 
                        spread=True)}