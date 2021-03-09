"""
A python wrapper for the gene prediction program AUGUSTUS.
"""

import os
import subprocess
from pkg_resources import resource_filename

from augustus.options.aug_options import *

__all__ = ['predict', 'train']

# can be overriden by user to specify path to AUGUSTUS or path to parameter file
AUGUSTUS_COMMAND = "augustus"
ETRAINING_COMMAND = "etraining"
PARAMETER_FILE = resource_filename('augustus.options', 'parameters.json')

# pygustus options
AUG_BINARY = 'augustus_binary'
AUG_PARAMETER_FILE = 'augustus_parameter_file'


def predict(*args, options=None, **kwargs):
    """
    Executes AUGUSTUS and passes the given parameters as command line arguments.

    TODO: parameter descritption
    """

    if AUG_BINARY in kwargs.keys():
        set_aug_command(kwargs[AUG_BINARY])
        kwargs.pop(AUG_BINARY, None)

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

    # execute AUGUSTUS with given options
    process = subprocess.Popen(
        [AUGUSTUS_COMMAND] + options.get_options(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    output = process.stdout.read()
    error = process.stderr.read()
    print(output)
    print(error)


def train():
    # TODO: implement
    pass


def set_aug_command(augustus_binary):
    if not os.path.exists(augustus_binary):
        raise ValueError(
            f'AUGUSTUS binaries cannot be found under specified path: {augustus_binary}.')
    else:
        global AUGUSTUS_COMMAND
        AUGUSTUS_COMMAND = augustus_binary


def set_parameter_file(parameter_file):
    if not os.path.exists(parameter_file):
        raise ValueError(
            f'AUGUSTUS parameter file cannot be found under specified path: {parameter_file}.')
    else:
        global PARAMETER_FILE
        PARAMETER_FILE = parameter_file
