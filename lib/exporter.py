import os
from typing import Dict, List
from lib.path import LOGS_PATH
import json

def dump_state(nb_iter, solutions: List[Dict[str, str]]):
    data_json = json.dumps(solutions)
    path = LOGS_PATH + "/" + str(nb_iter) + ".json"
    with open(path, "w") as f:
        f.write(data_json)
