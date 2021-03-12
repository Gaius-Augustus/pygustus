import json

class AugustusOption:

    def __init__(self, name, type, possible_values, description, usage, default_value, development):
        self.name = name
        self.development = development
        self.type = type
        self.possible_values = possible_values
        self.description = description
        self.usage = usage
        self.default_value = default_value
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
                raise ValueError(f'Empty list for parameter --{self.name} is not supported! Expected {self.type}.')

            for s in value:
                if not isinstance(s, str):
                    check_fail = True

        if check_fail:
            raise ValueError(
                f'Invalid value type for parameter --{self.name}! Expected {self.type}.')

    def get_name(self):
        return self.name

class AugustusOptions:
    _allowed_options = {}

    def __init__(self, *args, parameter_file, **kwargs):
        self._parameter_file = parameter_file
        self._options = {}
        self._args = []
        self.load_options()
        if len(args) > 0:
            self._args += args
        for option, value in kwargs.items():
            self.set_value(option, value)

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
        option.set_value(value)

        self._options[option_name] = option.value

    def get_value(self, option):
        if option not in self._options:
            raise ValueError('Unknown option: %s' % option)
        return self._options[option]

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
        with open(self._parameter_file, 'r') as file:
            options = json.load(file)

        for o in options:
            option = AugustusOption(o.get('name'), o.get('type'), o.get('possible_values'), o.get(
                'description'), o.get('usage'), o.get('default_value'), o.get('development'))
            self._allowed_options.update({option.name: option})
