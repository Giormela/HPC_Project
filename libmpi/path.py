import os

USER_ID = 0
MAKEFILE_PATH = ""
LOGS_PATH = ""

def find_logs_path(path):
    for root, directories, files in os.walk(path):
        if "datasets" in directories:
            return os.path.join(root, "datasets")
    return None

def set_user_id(id: int):
    global USER_ID
    global MAKEFILE_PATH
    global LOGS_PATH
    USER_ID = id
    MAKEFILE_PATH = "/usr/users/st76i/st76i_"+str(USER_ID)+"/iso3dfd-st7"
    LOGS_PATH = find_logs_path(MAKEFILE_PATH)

def get_makefile_path() -> str:
    global MAKEFILE_PATH
    return MAKEFILE_PATH

def get_logs_path() -> str:
    global LOGS_PATH
    return LOGS_PATH

