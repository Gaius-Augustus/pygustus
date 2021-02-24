import subprocess

import sys
from options.option import *

__all__ = ['run']

# can be overriden by user to specify path to AUGUSTUS or path to parameter file
AUGUSTUS_COMMAND = "augustus"
PARAMETER_FILE = 'options/parameters.json'


def run(*args, options=None, **kwargs):
    try:
        if options is None:
            options = AugustusOptions(*args, parameter_file = PARAMETER_FILE, **kwargs)
        else:
            for arg in args:
                options.add_argument(arg)
            for option, value in kwargs.items():
                options.set_value(option, value)
        options.check_dependencies()
    except ValueError as ve:
        print(ve)
        sys.exit()

    cmd = "%s %s" % (AUGUSTUS_COMMAND, options)
    process = subprocess.Popen(
        [AUGUSTUS_COMMAND] + options.get_options(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    # TODO improve output handling?

    output = process.stdout.read()
    error = process.stderr.read()

    print(output)
    print(error)
