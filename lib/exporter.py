from typing import Dict, List
import json

def dump_state(nb_iter, solutions: List[Dict[str, str]]):
    data_json = json.dumps(solutions)
    path = "visu/states/" + str(nb_iter)
    with open(path, "w") as f:
        f.write(data_json)
