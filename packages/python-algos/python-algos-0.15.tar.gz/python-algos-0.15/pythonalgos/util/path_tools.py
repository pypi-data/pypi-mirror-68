from pathlib import Path
import os
import shutil
import sys


def create_dir_in_user_home(dir, overwrite=True):
    if overwrite:
        clean_dir_in_user_home(dir)
    os.mkdir(Path(get_user_home(), dir))


def clean_dir_in_user_home(dir):
    if Path(str(get_user_home()), dir).exists() and \
            Path(str(get_user_home()), dir).is_dir():
        shutil.rmtree(Path(get_user_home(), dir))


def get_dir_in_user_home(dir):
    return str(Path(get_user_home(), dir))


def get_user_home():
    return str(Path.home())


def append_to_path(top_parent_package):
    """ Function that searches up the folder tree and finds the top package and
    then adds the package to sys.path

    Args:
        top_parent_package(str): The top parent package to find

    """

    name = os.path.realpath(__file__)
    while name.split("/")[-1] != top_parent_package:
        name = os.path.dirname(name)
    sys.path.append(os.path.dirname(name))
