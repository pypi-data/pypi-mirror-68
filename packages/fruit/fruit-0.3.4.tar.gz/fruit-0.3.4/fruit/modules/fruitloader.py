"""
This module implements the scan, loading and compiling of fruitconfig.py files.
"""

import os
import sys
import fruit.globals as glb
import importlib.util


def obtain_config(path: str) -> str:
    """
    Get the full path an existing fruit configuration file.

    If the given path is a direct path to a python script, it will be loaded directly.
    If the path is a directory, there are three cases to handle:
      * there is a subfulder `.fruit` with a file __init__.py:
         .fruit/__init__.py will be loaded
      * there is no subfolder `.fruit`, but there exists `fruitconfig.py`: fruitconfig.py will be loaded
      * none of the options was satisfied: return an error

    Parameters
    ----------
    `path` : str
        Directory path to a containing directory or file path

    Returns
    -------
    str
        Full path of the config.py

    Raises
    ------
    FileNotFoundError
        The fruitconfig.py file is not found in the current directory
    FileNotFoundError
        The given path is invalid
    """
    if os.path.exists(path):
        if os.path.isdir(path):
            if os.path.exists(os.path.join(path, glb.FRUIT_DIR_CONFIG)):
                # .fruit/__init__.py exists
                return os.path.join(path, glb.FRUIT_DIR_CONFIG)
            elif os.path.exists(os.path.join(path, glb.FRUITCONFIG_NAME)):
                # fruitconfig.py exists
                return os.path.join(path, glb.FRUITCONFIG_NAME)
            else:
                # No directory config found
                raise FileNotFoundError("There is no fruit configuration found in the selected path.")
        elif os.path.isfile(path) and path.endswith('.py'):
            # Direct path to a file
            return path
        else:
            raise FileNotFoundError("The given path is not a python file!")
    else:
        raise FileNotFoundError("The given path is invalid!")


def compile_config(path: str):
    """
    Compile the given python script at the given path and execute it to obtain decorated function properties.

    The given path will be added to the python path for the time of the execution. It may be removed afterwards to avoid
    module name collisions, when loading multiple modules.

    Parameters
    ----------
    path: str
        Path of the fruit configuration file to compile and load.

    """

    # Read the source code
    with open(path, 'r') as fp:
        source = fp.read()

    filename = os.path.basename(path)

    # Append the fruit config directory to the current python path, to import submodules
    directory = os.path.dirname(os.path.abspath(path))
    sys.path.append(directory)

    # Create a global namespace for the execution
    namespace = {}
    pyobj = compile(source=source, filename=filename, mode='exec')
    exec(pyobj, namespace, namespace)


def load(*path: str):
    """
    Load multiple instances of fruit configurations into the current running instance of fruit.

    Parameters
    ----------
    *path: str
        List of paths to load
    """

    # TODO: Implement loading of multiple fruit configs
    # TODO: Add load local option
    for each_path in path:
        configpath = obtain_config(each_path)
        compile_config(configpath)