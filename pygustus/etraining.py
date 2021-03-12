"""
A python wrapper for the training of AUGUSTUS.
"""

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
        util.set_path_to_bin(kwargs[AUG_BINARY], 'Etraining')
        kwargs.pop(AUG_BINARY, None)
    else:
        util.check_bin(ETRAINING_COMMAND)

    if AUG_PARAMETER_FILE in kwargs.keys():
        util.set_parameter_file(kwargs[AUG_PARAMETER_FILE])
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
