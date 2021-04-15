"""
A python wrapper for the gene prediction program AUGUSTUS.
"""

from pkg_resources import resource_filename

from pygustus.options.aug_options import *
import pygustus.util as util
import pygustus.fasta_methods as fm

__all__ = ['predict', 'config_get_bin',
           'config_set_bin', 'config_set_default_bin', 'show_fasta_info']


PARAMETER_FILE = resource_filename('pygustus.options', 'parameters.json')


def predict(*args, options=None, **kwargs):
    """
    Executes AUGUSTUS and passes the given parameters as command line arguments.

    TODO: parameter descritption
    """

    pygustus_options = util.get_options(
        *args, options=options, path_to_params=PARAMETER_FILE, program='pygustus', **kwargs)

    augustus_command = config_get_bin()
    tmp_path_to_bin = util.get_path_to_binary(pygustus_options, 'AUGUSTUS')
    if tmp_path_to_bin:
        augustus_command = tmp_path_to_bin

    util.check_bin(augustus_command)

    aug_options = util.get_options(
        *args, options=options, path_to_params=PARAMETER_FILE, program='augustus', **kwargs)

    jobs = pygustus_options.get_value_or_none('jobs')

    # check input file
    is_file, input_file = aug_options.get_input_filename()
    if is_file:
        if input_file:
            util.check_file(input_file)
        else:
            raise ValueError(f'Input file not specified.')

    if jobs:
        util.execute_bin_parallel(augustus_command, aug_options, jobs)
    else:
        util.execute_bin(augustus_command, aug_options.get_options())


def config_get_bin():
    """
    Reads the currently configured path to the executable of AUGUSTUS
    and returns it.

    Returns:
        The currently configured path to the executable of AUGUSTUS.
    """
    return util.get_config_item('augustus_bin')


def config_set_bin(value):
    """
    Updates the configured path to the executable of AUGUSTUS
    with the given value.

    Args:
        value (string): The path to the execuatble of AUGUSTUS.

    Raises:
        RuntimeError: If the given path does not exist or the file is
        not executable.
    """
    util.check_bin(value)
    util.set_config_item('augustus_bin', value)


def config_set_default_bin():
    """
    Sets the configured path to the AUGUSTUS executable to 'augustus'.
    This should exist if AUGUSTUS is properly installed on the system.
    """
    util.set_config_item('augustus_bin', 'augustus')


def show_fasta_info(inputfile):
    """
    This method outputs information about the contents of the passed file
    in fasta format. It is based on the Pearl script summarizeACGTcontent.pl.

    Args:
        inputfile (string): The file in fasta format.
    """
    fm.summarize_acgt_content(inputfile)