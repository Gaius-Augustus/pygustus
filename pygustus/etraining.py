"""
A python wrapper for the training of AUGUSTUS.
"""

import os
import subprocess
from pkg_resources import resource_filename

from pygustus.options.aug_options import *
import pygustus.util as util

__all__ = ['train']

# can be overriden by user to specify path to etraining or path to parameter file
# TODO: add config file to persist user specifications
ETRAINING_COMMAND = "etraining"
PARAMETER_FILE = resource_filename('pygustus.options', 'parameters.json')
# TODO: mark possible training parameters or create own config file?


# pygustus options
AUG_BINARY = 'etraining_binary'
AUG_PARAMETER_FILE = 'augustus_parameter_file'


def train(*args, options=None, **kwargs):
    """
    Executes etraining and passes the given parameters as command line arguments.

    TODO: parameter descritption
    """

    if AUG_BINARY in kwargs.keys():
        set_train_command(kwargs[AUG_BINARY])
        kwargs.pop(AUG_BINARY, None)
    else:
        util.check_bin(ETRAINING_COMMAND)

    if AUG_PARAMETER_FILE in kwargs.keys():
        set_parameter_file(kwargs[AUG_PARAMETER_FILE])
        kwargs.pop(AUG_PARAMETER_FILE, None)

    if options is None:
        options = AugustusOptions(
            *args, parameter_file=PARAMETER_FILE, **kwargs)
    else:
        for arg in args:
            options.add_argument(arg)
        for option, value in kwargs.items():
            options.set_value(option, value)

    util.execute_bin(ETRAINING_COMMAND, options.get_options())


def set_train_command(etraining_binary):
    if not os.path.exists(etraining_binary):
        raise ValueError(
            f'Etraining binaries cannot be found under specified path: {etraining_binary}.')

    global ETRAINING_COMMAND
    ETRAINING_COMMAND = etraining_binary


def set_parameter_file(parameter_file):
    if not os.path.exists(parameter_file):
        raise ValueError(
            f'AUGUSTUS parameter file cannot be found under specified path: {parameter_file}.')

    global PARAMETER_FILE
    PARAMETER_FILE = parameter_file
