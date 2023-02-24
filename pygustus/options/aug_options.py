import json
from distutils.util import strtobool


class AugustusOption:

    def __init__(self, name, type, possible_values, description, usage, default_value, development, exclude):
        self.name = name
        self.development = development
        self.type = type
        self.possible_values = possible_values
        self.description = description
        self.usage = usage
        self.default_value = default_value
        self.exclude = exclude
        self.value = None

    def set_value(self, value, check=True):
        if check:
            self.check_value(value)
        self.value = value

    def check_value(self, value):
        # TODO: check given value according to option properties
        self.check_values(value)
        self.check_type(value)

    def check_values(self, value):
        # TODO: check if property is iterable
        if not self.possible_values is None:
            if not value in self.possible_values:
                raise ValueError(
                    f'Invalid value for parameter --{self.name}! Expected {self.possible_values}.')

    def check_type(self, value):
        check_fail = False

        if self.type == 'string' and not isinstance(value, str):
            check_fail = True

        if self.type == 'int' and not isinstance(value, int):
            check_fail = True

        if self.type == 'float' and not isinstance(value, float):
            check_fail = True

        if self.type == 'bool' and not isinstance(value, bool):
            check_fail = True

        if self.type == 'list<string>' and not isinstance(value, list):
            check_fail = True
        elif self.type == 'list<string>' and isinstance(value, list):
            if not value:
                raise ValueError(
                    f'Empty list for parameter --{self.name} is not supported! Expected {self.type}.')

            for s in value:
                if not isinstance(s, str):
                    check_fail = True

        if check_fail:
            raise ValueError(
                f'Invalid value type for parameter --{self.name}! Expected {self.type}.')

    def get_name(self):
        return self.name

    def get_exclude(self):
        if self.exclude:
            return self.exclude
        else:
            return []


class AugustusOptions:
    _allowed_options = {}

    def __init__(self, *args, parameter_file, app, **kwargs):
        self._parameter_file = parameter_file
        self._options = {}
        self._app = app
        self._args = []
        self.load_options()
        if len(args) > 0:
            self._args += args
        for option, value in kwargs.items():
            self.set_value(option, value)
        self.setPygustusDefaultValues()

    def add_arguments(self, *args):
        self._args += args

    def add_argument(self, arg):
        self._args.append(arg)

    def get_arguments(self):
        return self._args

    def set_value(self, option_name, value):
        if option_name not in self._allowed_options.keys():
            raise ValueError(
                'Invalid Parameter for Augustus: %s' % option_name)

        option = self._allowed_options[option_name]

        if self._app == 'pygustus':
            if 'augustus' in option.get_exclude() and 'etraining' in option.get_exclude():
                option.set_value(value)
                self._options[option_name] = option.value
        else:
            if not self._app in option.get_exclude():
                option.set_value(value)
                self._options[option_name] = option.value

    def get_value(self, option):
        if option not in self._options:
            raise ValueError('Unknown option: %s' % option)
        return self._options[option]

    def get_value_or_none(self, name):
        return self._options.get(name)

    def remove(self, name):
        if name in self._options:
            del self._options[name]

    def get_options(self):
        opts = []
        for option, value in self._options.items():
            if isinstance(value, list):
                opts.append("--%s=%s" % (option, ','.join(value)))
            else:
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
        self._allowed_options = load_allowed_options(self._parameter_file)

    def get_input_filename(self):
        if len(self._args) == 1:
            if (self._args[0].startswith('--')):
                return False, None
            else:
                return True, self._args[0]
        else:
            return False, None

    def set_input_filename(self, name):
        if len(self._args) == 1:
            self._args[0] = name
        else:
            # TODO: throw an error?
            print('Could not set filename!')

    def setPygustusDefaultValues(self):
        for key, item in self._allowed_options.items():
            if not self.get_value_or_none(key) and item.default_value and \
                    'augustus' in item.get_exclude() and \
                    'etraining' in item.get_exclude():
                if item.type == 'int':
                    self.set_value(key, int(item.default_value))
                elif item.type == 'bool':
                    self.set_value(key, bool(strtobool(item.default_value)))
                elif item.type == 'float':
                    self.set_value(key, float(item.default_value))
                else:
                    self.set_value(key, item.default_value)


def load_allowed_options(parameter_file, program=None):
    allowed_options = dict()
    with open(parameter_file, 'r') as file:
        options = json.load(file)

    for o in options:
        option = AugustusOption(o.get('name'), o.get('type'), o.get('possible_values'), o.get(
            'description'), o.get('usage'), o.get('default_value'), o.get('development'), o.get('exclude_apps'))

        if program == 'pygustus':
            if 'augustus' in option.get_exclude() and 'etraining' in option.get_exclude():
                allowed_options.update({option.get_name(): option})
        elif program:
            if not program in option.get_exclude():
                allowed_options.update({option.get_name(): option})
        else:
            allowed_options.update({option.get_name(): option})

    return allowed_options
