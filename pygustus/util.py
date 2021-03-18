import subprocess
import os
from shutil import which
from pygustus.options.aug_options import *


def execute_bin(cmd, options):
    # execute given binary with given options
    rc = process = subprocess.Popen(
        [cmd] + options, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    output = process.stdout.read()
    error = process.stderr.read()
    print(output)
    print(error)
    if rc != 0:
        print(f'Unexpected returncode {rc}!')


def check_bin(bin):
    if which(bin) is None:
        raise RuntimeError(
            f'{bin} cannot be found or is not executable!')


def get_options(*args, options, path_to_params, program, **kwargs):
    if options is None:
        options = AugustusOptions(
            *args, parameter_file=path_to_params, app=program, **kwargs)
    else:
        for arg in args:
            options.add_argument(arg)
        for option, value in kwargs.items():
            options.set_value(option, value)
    return options


def get_path_to_binary(options, program):
    bin = options.get_value_or_none('path_to_bin')
    if bin and not os.path.exists(bin):
        raise ValueError(
            f'{program} binaries cannot be found under specified path: {bin}.')
    return bin
