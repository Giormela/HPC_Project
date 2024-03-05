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
           "simd": Param("simd", ["avx2"], "avx2"),
           "n": Param("n", [256, 512], 256),
           "num_threads": Param("num_threads", [i for i in range(1, 33)], 32),
           "n_size": Param("n_size", [16, 32, 64], 32)}