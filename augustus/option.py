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

    def set_value(self, value):
        if self.check_value(value):
            self.value = value
    
    def check_value(self, value):
        #TODO: check given value according to option properties
        values = self.check_values(value)

        if values:
            return True
        else:
            return False

    def check_values(self, value):
        # TODO: check if property is iterable
        if not self.possible_values is None:
            print(self.possible_values)
            if value in self.possible_values:
                return True
            else:
                return False
        else:
            return True

    #def check_dependencies(): #TODO: possible dependency check after all otpions are instantiated