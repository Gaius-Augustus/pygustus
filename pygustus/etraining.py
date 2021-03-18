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


def train(*args, options=None, **kwargs):
    """
    Executes etraining and passes the given parameters as command line arguments.

    TODO: parameter descritption
    """

    pygustus_options = util.get_options(
        *args, options=options, path_to_params=PARAMETER_FILE, program='pygustus', **kwargs)

    tmp_path_to_bin = util.get_path_to_binary(pygustus_options, 'ETRAINING')
    if tmp_path_to_bin:
        global ETRAINING_COMMAND
        ETRAINING_COMMAND = tmp_path_to_bin

    util.check_bin(ETRAINING_COMMAND)

    aug_options = util.get_options(
        *args, options=options, path_to_params=PARAMETER_FILE, program='etraining', **kwargs)

    util.execute_bin(ETRAINING_COMMAND, aug_options.get_options())
