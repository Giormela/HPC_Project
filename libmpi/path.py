import os

USER_ID = 0
MAKEFILE_PATH = ""
LOGS_PATH = ""
REPOSITORY_PATH = ""

def find_logs_path(path):
    print(path)
    if not os.path.exists(path):
        os.mkdir(path)
    for root, directories, files in os.walk(path):
        if "datasets" in directories:
            return os.path.join(root, "datasets")
    raise ValueError("Problem in building paths: probably the user id equal to "+str(USER_ID)+" is wrong.")

def find_makefile_path(path):
    for root, directories, files in os.walk(path):
        if "iso3dfd-st7" in directories:
            return os.path.join(root, "iso3dfd-st7")
    raise ValueError("Problem in building paths: probably the user id equal to "+str(USER_ID)+" is wrong.")

def set_user_id(id: int):
    global USER_ID
    global MAKEFILE_PATH
    global LOGS_PATH
    global REPOSITORY_PATH
    USER_ID = id
    REPOSITORY_PATH = os.getcwd()
    MAKEFILE_PATH = find_makefile_path("/usr/users/st76i/st76i_"+str(USER_ID))
    path = "/Dashboard/main/datasets"
    if not os.path.exists("."+path):
        os.makedirs("."+path)
    LOGS_PATH = REPOSITORY_PATH + path

def get_makefile_path() -> str:
    return MAKEFILE_PATH

def get_logs_path() -> str:
    return LOGS_PATH

def get_home_path() -> str:
    return REPOSITORY_PATH

