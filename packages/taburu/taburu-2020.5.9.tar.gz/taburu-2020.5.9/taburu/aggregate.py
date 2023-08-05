# Copyright (c) 2019 Toyota Research Institute

import abc
from taburu.table import ParameterTable, HashedParameterArray
from taburu.event import ParametersAdded


class Aggregate(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def from_events(cls, events):
        pass


class ParameterTables(Aggregate):
    @classmethod
    def from_events(cls, events):
        pass


# More lightweight aggregate with just the names
class ParameterTableNames(HashedParameterArray, Aggregate):
    def __init__(self, parameter_table_names):
        super(ParameterTableNames, self).__init__(parameter_table_names)

    @classmethod
    def from_events(cls, events):
        add_parameter_events = filter(lambda x: isinstance(x, ParametersAdded), events)
        parameter_table_names = [event.table_name for event in add_parameter_events]
        return cls(parameter_table_names)
