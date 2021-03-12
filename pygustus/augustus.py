"""
A python wrapper for the gene prediction program AUGUSTUS.
"""

from pkg_resources import resource_filename

from pygustus.options.aug_options import *
import pygustus.util as util

__all__ = ['predict']

# can be overriden by user to specify path to AUGUSTUS or path to parameter file
# TODO: add config file to persist user specifications
AUGUSTUS_COMMAND = "augustus"
PARAMETER_FILE = resource_filename('pygustus.options', 'parameters.json')

# pygustus options
AUG_BINARY = 'augustus_binary'
AUG_PARAMETER_FILE = 'augustus_parameter_file'


def predict(*args, options=None, **kwargs):
    """
    Executes AUGUSTUS and passes the given parameters as command line arguments.

    TODO: parameter descritption
    """

    if AUG_BINARY in kwargs.keys():
        util.set_path_to_bin(kwargs[AUG_BINARY], 'AUGUSTUS')
        kwargs.pop(AUG_BINARY, None)
    else:
        util.check_bin(AUGUSTUS_COMMAND)

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

    util.execute_bin(AUGUSTUS_COMMAND, options.get_options())
