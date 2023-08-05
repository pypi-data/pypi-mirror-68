import os, shutil

def check_path(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)




    