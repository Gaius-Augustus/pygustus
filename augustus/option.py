class Option:

    def __init__(self, name, type, possible_values, description, usage, default_value, dependencies):
        self.name = name
        self.type = type
        self.possible_values = possible_values
        self.description = description
        self.usage = usage
        self.default_value = default_value
        self.dependencies = dependencies
        self.value = None

    def set_value(self, value, check=True):
        if check:
            self.check_value(value)
        self.value = value
    
    def check_value(self, value):
        #TODO: check given value according to option properties
        self.check_values(value)
        self.check_type(value)

    def check_values(self, value):
        # TODO: check if property is iterable
        if not self.possible_values is None:
            if not value in self.possible_values:
                raise ValueError(f'Invalid value for parameter --{self.name}! Expected {self.possible_values}.')

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

        if check_fail:
             raise ValueError(f'Invalid value type for parameter --{self.name}! Expected {self.type}.')


    def get_dependencies(self):
        return self.dependencies

    def get_name(self):
        return self.name
