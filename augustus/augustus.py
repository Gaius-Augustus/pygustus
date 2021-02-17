import subprocess
import sys
import json

__all__ = ['run']

# can be overriden by user to specify path to AUGUSTUS
AUGUSTUS_COMMAND = "augustus"

parameter_file = '../options/parameters.json'

class AugustusOptions:
    # can easily be read from file, validation info could also be stored there - could also be ignored.
    _allowed_options = []

    def __init__(self, *args, **kwargs):
        self.load_options()
        self._options = {}
        self._args = []
        if len(args) > 0:
            self._args += args
        for option, value in kwargs.items():
            self.set_value(option, value)

    def add_arguments(self, *args):
        self._args += args

    def add_argument(self, arg):
        print(arg)
        self._args.append(arg)

    def get_arguments(self):
        return self._args

    def set_value(self, option, value):
        print(option)
        if option not in self._allowed_options:
            raise ValueError('Invalid Parameter for Augustus: %s' % option)
            # TODO disable check for now
            # pass
        # TODO possibly also validate type of option and value here
        self._options[option] = value

    def get_value(self, option):
        if option not in self._options:
            raise ValueError('Unknown option: %s' % option)
        return self._options[option]

    def get_options(self):
        opts = []
        for option, value in self._options.items():
            opts.append("--%s=%s" % (option, value))
        opts += self._args
        return opts

    def __str__(self):
        optstr = ""
        for option, value in self._options.items():
            optstr += "--%s=%s " % (option, value)
        if len(self._args):
            optstr += " ".join(self._args)
        return optstr

    def load_options(self):
        with open(parameter_file, 'r') as file:
                options = json.load(file)

        # Currently only the name of the option is used, other properties will follow
        for o in options:
            self._allowed_options.append(o['name'])


def run(*args, options=None, **kwargs):
    if options is None:
        options = AugustusOptions(*args, **kwargs)
    else:
        for arg in args:
            options.add_argument(arg)
        for option, value in kwargs.items():
            options.set_value(option, value)

    cmd = "%s %s" % (AUGUSTUS_COMMAND, options)
    process = subprocess.Popen(
        [AUGUSTUS_COMMAND] + options.get_options(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    # TODO better output handling including stderr
    #for line in process.stdout:
    #    sys.stdout.write(line)

    output = process.stdout.read()
    error = process.stderr.read()

    print(output)
    print(error)
