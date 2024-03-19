from typing import Dict, List
from libmpi.path import LOGS_PATH
import csv
import os

def find_logs_path(path):
    for root, directories, files in os.walk(path):
        if "datasets" in directories:
            return os.path.join(root, "datasets")
    return None

CONV_DICT = {"olevel": "opti_flag_id", 
             "simd": "vecto_flag_id",
             "num_threads": "n_threads",
             "n1_size": "x_tbs",
             "n2_size": "y_tbs",
             "n3_size": "z_tbs",
             "gflops": "rank"}


def dump_state(nb_iter, solutions: List[Dict[str, str]]):
    solutions = convert_labels(solutions)
    print("Logs file: ", LOGS_PATH)
    filename = LOGS_PATH + "/data" + str(nb_iter) + ".csv"
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=solutions[0].keys())
        writer.writeheader()
        for solution in solutions:
            writer.writerow(solution)


def convert_labels(solutions: List[Dict[str, str]]):
    res = []
    for solution in solutions:
        new_sol = {}
        for tuple in solution.items():
            new_sol[CONV_DICT[tuple[0]]] = tuple[1]
        res.append(new_sol)
    return res
