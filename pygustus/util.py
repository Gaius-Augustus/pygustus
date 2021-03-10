import subprocess
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
