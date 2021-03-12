import subprocess
import os
from shutil import which


def execute_bin(cmd, options):
    # execute given binary with given options
    process = subprocess.Popen(
        [cmd] + options, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    output = process.stdout.read()
    error = process.stderr.read()
    print(output)
    print(error)


def check_bin(bin):
    if which(bin) is None:
        raise RuntimeError(
            f'Executable {bin} cannot be found! Make sure the program is installed correctly or specify a path.')


def set_path_to_bin(bin_file, program):
    if not os.path.exists(bin_file):
        raise ValueError(
            f'{program} binaries cannot be found under specified path: {bin_file}.')

    global ETRAINING_COMMAND
    ETRAINING_COMMAND = bin_file


def set_parameter_file(parameter_file):
    if not os.path.exists(parameter_file):
        raise ValueError(
            f'AUGUSTUS parameter file cannot be found under specified path: {parameter_file}.')

    global PARAMETER_FILE
    PARAMETER_FILE = parameter_file
