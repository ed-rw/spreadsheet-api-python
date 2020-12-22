
from abc import ABC, abstractmethod

import config

class Command(ABC):
    pass


class Query(ABC):
    pass


class UnsupportedOperationForBackend(NotImplementedError):
    pass


class CreateSpreadsheet(Command, ABC):

    def __init__(self, settings: config.Settings, id: str, name: str):
        self.settings = settings
        self.id = id
        self.name = name

    @abstractmethod
    def execute(self):
        pass


class RetrieveSpreadsheets(Query, ABC):
    def __init__(self, settings: config.Settings):
        self.settings = settings

    @abstractmethod
    def retrieve_data(self):
        pass


class CommandFactory(ABC):
    command_map: dict

    def __init__(self, settings):
        self.settings = settings

    def build(self, command_name: str, *args, **kwargs):
        try:
            return self.command_map[command_name](*args, **kwargs)
        except KeyError:
            raise UnsupportedOperationForBackend()


class QueryFactory(ABC):
    query_map: dict

    def __init__(self, settings):
        self.settings = settings

    def build(self, query_name: str, *args, **kwargs):
        try:
            return self.query_map[query_name](*args, **kwargs)
        except KeyError:
            raise UnsupportedOperationForBackend()
