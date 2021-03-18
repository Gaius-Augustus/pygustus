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


def predict(*args, options=None, **kwargs):
    """
    Executes AUGUSTUS and passes the given parameters as command line arguments.

    TODO: parameter descritption
    """

    pygustus_options = util.get_options(
        *args, options=options, path_to_params=PARAMETER_FILE, program='pygustus', **kwargs)

    tmp_path_to_bin = util.get_path_to_binary(pygustus_options, 'AUGUSTUS')
    if tmp_path_to_bin:
        global AUGUSTUS_COMMAND
        AUGUSTUS_COMMAND = tmp_path_to_bin

    util.check_bin(AUGUSTUS_COMMAND)

    aug_options = util.get_options(
        *args, options=options, path_to_params=PARAMETER_FILE, program='augustus', **kwargs)

    util.execute_bin(AUGUSTUS_COMMAND, aug_options.get_options())
