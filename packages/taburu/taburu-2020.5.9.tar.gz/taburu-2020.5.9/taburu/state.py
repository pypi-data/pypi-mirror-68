# Copyright (c) 2019 Toyota Research Institute
import abc
from taburu.event import ParametersAdded, MethodAdded
from taburu.table import ParameterTable
from indexed import IndexedOrderedDict


class State(abc.ABC):
    @abc.abstractmethod
    def apply(self, event):
        pass


class TaburuState(State):
    def __init__(self):
        self.parameters = IndexedOrderedDict()
        self.methods = IndexedOrderedDict()

    def apply(self, event):
        if isinstance(event, ParametersAdded):
            if event.table_name in self.parameters:
                self.parameters[event.table_name].append(event.parameters)
            else:
                self.parameters[event.table_name] = ParameterTable(event.parameters)
        elif isinstance(event, MethodAdded):
            if self.methods.get(event.name) is None:
                self.methods[event.name] = event.parameter_indices
            else:
                print("Method name already exists")
                return False
        return True

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        parameters = ['{} {}: {}'.format(n, parameter_name, len(table))
                      for n, (parameter_name, table) in
                      enumerate(self.parameters.items())]
        methods = ["{}: {}".format(method_name, parameters)
                   for method_name, parameters in self.methods.items()]
        output = "Parameters:\n   "
        output += "\n   ".join(parameters)
        output += "\nMethods:\n   "
        output += "\n   ".join(methods)
        return output
