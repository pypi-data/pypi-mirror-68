# Copyright (c) 2019 Toyota Research Institute
from taburu.state import TaburuState
from taburu.event import Event, ParametersAdded, MethodAdded
from monty.json import MSONable


class AddParameterCommanded(Event, MSONable):
    def __init__(self, table_name, parameters, time=None):
        self.table_name = table_name
        self.parameters = parameters
        super(AddParameterCommanded, self).__init__(time)

    def as_dict(self):
        return {
            "@class": self.__class__.__name__,
            "@module": self.__class__.__module__,
            "table_name": self.table_name,
            "parameters": self.parameters,
            "time": self._time
        }


class AddMethodCommanded(Event, MSONable):
    """Event schema is the same except with names instead of params"""
    def __init__(self, name, parameter_names, time=None):
        self.name = name
        self.parameter_names = parameter_names
        super(AddMethodCommanded, self).__init__(time)

    def as_dict(self):
        return {
            "@class": self.__class__.__name__,
            "@module": self.__class__.__module__,
            "name": self.name,
            "parameter_names": self.parameter_names,
            "time": self._time
        }


class TaburuCommandProcessor(object):
    def __init__(self, command_channel, event_channel=None,
                 state=None):
        self.state = state or TaburuState()
        self.command_channel = command_channel
        self.event_channel = event_channel

    def publish(self, event):
        self.event_channel.publish(event)

    def process_command(self, command):
        if isinstance(command, AddParameterCommanded):
            parameters_added = ParametersAdded(command.table_name,
                                               command.parameters)
            if self.state.apply(parameters_added):
                self.publish(parameters_added)
        if isinstance(command, AddMethodCommanded):
            # look for methods in state
            try:
                state_parameter_names = self.state.parameters.keys()
                parameter_indices = tuple(
                    [state_parameter_names.index(parameter_name)
                     for parameter_name in command.parameter_names]
                )
            except ValueError as e:
                print("Parameter name mismatch: {}".format(e))
                return False
            method_added = MethodAdded(command.name, tuple(parameter_indices))
            if self.state.apply(method_added):
                self.publish(method_added)
        return True

    def run(self, iterations=None, poll_time=10):
        commands = self.command_channel.subscribe(
            iterations=iterations, poll_time=poll_time)
        for command in commands:
            self.process_command(command)
            print(self.state)
