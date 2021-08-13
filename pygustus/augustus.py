"""
A python wrapper for the gene prediction program AUGUSTUS.
"""

from pkg_resources import resource_filename
from pygustus.options import aug_options
import pygustus.util as util
import pygustus.fasta_methods as fm
import gzip
import os
import textwrap

__all__ = ['predict', 'config_get_bin',
           'config_set_bin', 'config_set_default_bin', 'show_fasta_info',
           'show_aug_help', 'show_aug_paramlist', 'show_species_info', 'help']


PARAMETER_FILE = util.get_path_to_parameters_file()
MIN_AUG_VERSION = '3.3.2'


def predict(*args, options=None, **kwargs):
    """Executes the binary of AUGUSTUS.
    
    For the execution the given parameters are passed as
    command line arguments.

    Args:
        *args (tuple): Exactly one argument should be passed here.
            Either the queryfilename or one of the help calls of
            AUGUSTUS (--help, --pramlist).
        options (AugustusOptions): Optional; If an instance of AugustusOptions
            is passed, it will be used for the call. Otherwise, a new instance
            is created based on the passed arguments (the default is None).
        **kwargs (dict): Arguments for AUGUSTUS or Pygustus as dict: lists with
            possible parameters can be obtained from the help methods or 
            the Pygustus README (only Pygustus parameters).
    """

    util.set_tmp_config_path(options, **kwargs)

    pygustus_options = util.get_options(
        *args, options=options, path_to_params=PARAMETER_FILE, program='pygustus', **kwargs)

    augustus_command = config_get_bin()
    tmp_path_to_bin = util.get_path_to_binary(pygustus_options, 'AUGUSTUS')
    if tmp_path_to_bin:
        augustus_command = tmp_path_to_bin

    util.check_bin(augustus_command)
    util.check_aug_version(augustus_command, MIN_AUG_VERSION)

    aug_options = util.get_options(
        *args, options=options, path_to_params=PARAMETER_FILE, program='augustus', **kwargs)

    jobs = pygustus_options.get_value_or_none('jobs')
    chunksize = pygustus_options.get_value_or_none('chunksize')
    overlap = pygustus_options.get_value_or_none('overlap')
    partition_hints = pygustus_options.get_value_or_none('partitionHints')
    minsize = pygustus_options.get_value_or_none('minSplitSize')
    partition_sequences = pygustus_options.get_value_or_none(
        'partitionLargeSeqeunces')
    debug_dir = pygustus_options.get_value_or_none('debugOutputDir')
    max_seq_size = pygustus_options.get_value_or_none('maxSeqSize')

    # check input file
    zip = False
    is_set, input_file = aug_options.get_input_filename()
    if is_set:
        if input_file:
            util.check_file(input_file)
        else:
            raise ValueError(f'Input file not specified.')

        # unzip if gz file is given
        f_name, f_ext = os.path.splitext(input_file)
        if f_ext == '.gz':
            nf = open(f_name, 'wb')
            with gzip.open(input_file) as f:
                bindata = f.read()
                nf.write(bindata)
            nf.close()
            aug_options.set_input_filename(f_name)
            zip = True

    if jobs and jobs > 1:
        util.execute_bin_parallel(
            augustus_command, aug_options, jobs, chunksize, overlap, partition_sequences, partition_hints, minsize, max_seq_size, debug_dir)
    else:
        print(f'Execute AUGUSTUS with given options.')

        util.execute_bin(augustus_command, aug_options.get_options())
        
        outfile = aug_options.get_value_or_none('outfile')
        if outfile:
            print(f'Output written to: {outfile}')

    if zip:
        os.remove(f_name)


def config_get_bin():
    """Returns currently configured path to the executable of AUGUSTUS.

    Returns:
        string: The currently configured path to the executable of AUGUSTUS.
    """
    return util.get_config_item('augustus_bin')


def config_set_bin(value):
    """Updates the configured path to the executable of AUGUSTUS.

    Args:
        value (string): The path to the execuatble of AUGUSTUS as string.

    Raises:
        RuntimeError: If the given path does not exist or the file
        is not executable.
    """
    util.check_bin(value)
    util.set_config_item('augustus_bin', value)


def config_set_default_bin():
    """Sets the configured path to the AUGUSTUS executable to 'augustus'.

    This should exist if AUGUSTUS is properly installed on the system.
    """
    util.set_config_item('augustus_bin', 'augustus')


def show_fasta_info(inputfile):
    """Outputs information about a fasta file.
    
    This method outputs information about the contents of the passed file
    in fasta format. It is based on the Pearl script summarizeACGTcontent.pl.

    Args:
        inputfile (string): Path to the file in fasta format as string.
    """
    fm.summarize_acgt_content(inputfile)


def show_aug_help():
    """Shows the help output of AUGUSTUS.
    """
    predict('--help')


def show_aug_paramlist():
    """Shows possible parameter names of AUGUSTUS.
    """
    predict('--paramlist')


def show_species_info():
    """Shows species information of AUGUSTUS.
    """
    predict('--species=help')


def help():
    """Shows usage information.
    """

    help_msg = """usage:
augustus.predict(queryfilename, species='SPECIES', [augustus_parameters], [pygustus_parameters])

'queryfilename' is the filename (including relative path) to the file
containing the query sequence(s) in fasta format.

SPECIES is an identifier for the species.
Use augustus.show_species_info() to see a list.

augustus_parameters are all possible parameters for AUGUSTUS.
Use augustus.show_aug_help() to find more information or
augustus.show_aug_paramlist() to see a list.

pygustus_parameters:

"""
    pygustus_options = aug_options.load_allowed_options(
        PARAMETER_FILE, program='pygustus')
    for opt in pygustus_options.values():
        help_msg += f'{opt.name} ({opt.type})\n'
        if opt.description:
            lines = textwrap.wrap(opt.description)
            help_msg += '  description:\n'
            for l in lines:
                help_msg += f'    {l} \n'
        if opt.possible_values:
            help_msg += f'  possible values: {opt.possible_values} \n'
        if opt.default_value:
            help_msg += f'  default value: {opt.default_value} \n'
        help_msg += '\n'

    print(help_msg.rstrip())
