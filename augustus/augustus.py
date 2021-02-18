import subprocess
import json
from option import Option

__all__ = ['run']

# can be overriden by user to specify path to AUGUSTUS
AUGUSTUS_COMMAND = "augustus"

parameter_file = '../options/parameters.json'


class AugustusOptions:
    _allowed_options = {}

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

    def set_value(self, option_name, value):
        print(option_name)
        if option_name not in self._allowed_options.keys():
            raise ValueError(
                'Invalid Parameter for Augustus: %s' % option_name)
        # TODO possibly also validate type of option and value here
        option = self._allowed_options[option_name]
        option.set_value(value)
        print(option.value)
        #TODO: validation error handling
        self._options[option_name] = option.value

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

        for o in options:
            option = Option(o.get('name'), o.get('type'), o.get('values'), o.get(
                'description'), o.get('usage'), o.get('default'), o.get('dependencies'))
            self._allowed_options.update({option.name: option})


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
    # TODO improve output handling?

    output = process.stdout.read()
    error = process.stderr.read()

    print(output)
    print(error)
