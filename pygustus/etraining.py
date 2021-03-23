"""
A python wrapper for the training of AUGUSTUS.
"""

from pkg_resources import resource_filename

from pygustus.options.aug_options import *
import pygustus.util as util

__all__ = ['train', 'config_get_bin',
           'config_set_bin', 'config_set_default_bin']


PARAMETER_FILE = resource_filename('pygustus.options', 'parameters.json')


def train(*args, options=None, **kwargs):
    """
    Executes etraining and passes the given parameters as command line arguments.

    TODO: parameter descritption
    """

    pygustus_options = util.get_options(
        *args, options=options, path_to_params=PARAMETER_FILE, program='pygustus', **kwargs)

    etraining_command = config_get_bin()
    tmp_path_to_bin = util.get_path_to_binary(pygustus_options, 'ETRAINING')
    if tmp_path_to_bin:
        etraining_command = tmp_path_to_bin

    util.check_bin(etraining_command)

    aug_options = util.get_options(
        *args, options=options, path_to_params=PARAMETER_FILE, program='etraining', **kwargs)

    util.execute_bin(etraining_command, aug_options.get_options())


def config_get_bin():
    return util.get_config_item('etraining_bin')


def config_set_bin(value):
    util.set_config_item('etraining_bin', value)


def config_set_default_bin():
    util.set_config_item('etraining_bin', 'etraining')
