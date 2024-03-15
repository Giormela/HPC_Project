import os

USER_ID = input("Digit your user code: ")
MAKEFILE_PATH = "/usr/users/st76i/st76i_"+USER_ID+"/iso3dfd-st7"

def find_logs_path(path):
    for root, directories, files in os.walk(path):
        if "datasets" in directories:
            return os.path.join(root, "datasets")
    return None

LOGS_PATH = find_logs_path(MAKEFILE_PATH)
