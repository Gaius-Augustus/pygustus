import subprocess
import os
import json
import sys
from shutil import which
from pygustus.options.aug_options import *
from pkg_resources import resource_filename


def execute_bin_parallel(cmd, aug_options, jobs):
    print(f'Execute AUGUSTUS with {jobs} jobs in parallel.')

    input_file = aug_options.get_input_filename()
    if input_file:
        size = os.path.getsize(input_file)
    else:
        print('Input file is not specified!')
        sys.exit()

    print(f'Size of input file: {size} bytes.')


def execute_bin(cmd, options, print_err=True, std_out_file=None, error_out_file=None, mode='w'):
    # execute given binary with given options

    if std_out_file and error_out_file and mode:
        with open(std_out_file, mode) as file:
            with open(error_out_file, mode) as errfile:
                process = subprocess.Popen(
                    [cmd] + options,
                    stdout=file,
                    stderr=errfile,
                    universal_newlines=True)
    elif std_out_file and mode:
        with open(std_out_file, mode) as file:
            process = subprocess.Popen(
                [cmd] + options,
                stdout=file,
                stderr=subprocess.PIPE,
                universal_newlines=True)
    else:
        process = subprocess.Popen(
            [cmd] + options,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True)

    rc = process.wait()

    if not std_out_file:
        output = process.stdout.read()
        print(output)

    if print_err and process.stderr:
        error = process.stderr.read()
        print(error)

    if rc != 0:
        print(f'Unexpected returncode {rc}!')


def check_bin(bin):
    if which(bin) is None:
        raise RuntimeError(
            f'{bin} cannot be found or is not executable!')


def check_file(inputfile):
    if not os.path.exists(inputfile):
        raise ValueError(f'Could not open {inputfile}')


def mkdir_if_not_exists(dir):
    if not os.path.exists(dir):
        os.makedirs(dir, exist_ok=True)


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


def get_config_item(name):
    config_file = resource_filename('pygustus', 'config.json')
    with open(config_file, 'r') as file:
        config = json.load(file)

    return config.get(name)


def set_config_item(name, value):
    config_file = resource_filename('pygustus', 'config.json')
    with open(config_file, 'r+') as file:
        config = json.load(file)
        config.update({name: value})
        file.seek(0)
        file.truncate()
        json.dump(config, file, indent=4, sort_keys=False)
