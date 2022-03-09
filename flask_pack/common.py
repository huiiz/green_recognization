import shutil
import os
def clear_folds(path: str, folds: tuple):
    try:
        for fold in folds:
            shutil.rmtree(f'{path}/{fold}')
            os.mkdir(f'{path}/{fold}')
        return True
    except:
        return False

def make_folds(path, folds):
    try:
        for fold in folds:
            os.mkdir(f'{path}/{fold}')
        return True
    except:
        return False

def del_folds(path, folds):
    try:
        for fold in folds:
            shutil.rmtree(f'{path}/{fold}')
        return True
    except:
        return False