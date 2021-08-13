"""
A python wrapper for the training of AUGUSTUS.
"""

from pkg_resources import resource_filename

from pygustus.options.aug_options import *
import pygustus.util as util

__all__ = ['train', 'config_get_bin',
           'config_set_bin', 'config_set_default_bin']


PARAMETER_FILE = util.get_path_to_parameters_file()


def train(*args, options=None, **kwargs):
    """
    Executes etraining and passes the given parameters as command line arguments.

    Args:
        *args (tuple): Only the the queryfilename should be passed here.
        options (AugustusOptions): Optional; If an instance of
            AugustusOptions is passed, it will be used for the call.
            Otherwise, a new instance is created based on the passed arguments
            (the default is None).
        **kwargs (dict): Arguments for Etraining or Pygustus: lists with
            possible parameters can be obtained from the help methods or 
            the Pygustus README (only Pygustus parameters).
    """

    util.set_tmp_config_path(options, **kwargs)

    pygustus_options = util.get_options(
        *args, options=options, path_to_params=PARAMETER_FILE, program='pygustus', **kwargs)

    etraining_command = config_get_bin()
    tmp_path_to_bin = util.get_path_to_binary(pygustus_options, 'ETRAINING')
    if tmp_path_to_bin:
        etraining_command = tmp_path_to_bin

    util.check_bin(etraining_command)

    aug_options = util.get_options(
        *args, options=options, path_to_params=PARAMETER_FILE, program='etraining', **kwargs)

    # check input file
    is_file, input_file = aug_options.get_input_filename()
    if is_file:
        if input_file:
            util.check_file(input_file)
        else:
            raise ValueError(f'Input file not specified.')

    util.execute_bin(etraining_command, aug_options.get_options())


def config_get_bin():
    """Outputs currently configured path to the executable of etraining.

    Returns:
        string: The currently configured path to the executable of etraining.
    """
    return util.get_config_item('etraining_bin')


def config_set_bin(value):
    """ Updates the configured path to the executable of etraining.

    Args:
        value (string): The path to the execuatble of etraining.

    Raises:
        RuntimeError: If the given path does not exist or the file
        is not executable.
    """
    util.check_bin(value)
    util.set_config_item('etraining_bin', value)


def config_set_default_bin():
    """Sets the configured path to the etraining executable to 'etraining'.

    This executable should exist if AUGUSTUS is properly installed
    on the system.
    """
    util.set_config_item('etraining_bin', 'etraining')
