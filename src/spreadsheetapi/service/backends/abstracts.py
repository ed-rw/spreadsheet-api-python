from abc import ABC, abstractmethod
from backends import commands, queries
import config


class CommandHandler(ABC):
    @abstractmethod
    async def execute(self):
        raise NotImplementedError()


class QueryHandler(ABC):
    @abstractmethod
    async def retrieve_data(self):
        raise NotImplementedError()


class CommandFactory(ABC):
    command_map = {
        "CreateSpreadsheet": commands.CreateSpreadsheet,
        "DeleteSpreadsheet": commands.DeleteSpreadsheet,
        "UpdateSpreadsheet": commands.UpdateSpreadsheet,
        "UpdateCell": commands.UpdateCell,
        "DeleteCell": commands.DeleteCell,
    }

    def __init__(self, settings: config.Settings):
        self.settings = settings

    @abstractmethod
    def get_handler(self, command_name: str):
        raise NotImplementedError()

    def build(self, command_name: str, *args, **kwargs):
        try:
            return (
                self.command_map[command_name](*args, **kwargs),
                self.get_handler(command_name),
            )
        except KeyError:
            raise UnsupportedOperationForBackend()


class QueryFactory(ABC):
    query_map = {
        "RetrieveSpreadsheets": queries.RetrieveSpreadsheets,
        "RetrieveSpreadsheet": queries.RetrieveSpreadsheet,
        "RetrieveSpreadsheetView": queries.RetrieveSpreadsheetView,
        "RetrieveCell": queries.RetrieveCell,
        "RetrieveCells": queries.RetrieveCells,
    }

    def __init__(self, settings: config.Settings):
        self.settings = settings

    @abstractmethod
    def get_handler(self, query_name: str):
        raise NotImplementedError()

    def build(self, query_name: str, *args, **kwargs):
        try:
            return (
                self.query_map[query_name](*args, **kwargs),
                self.get_handler(query_name),
            )
        except KeyError:
            raise UnsupportedOperationForBackend()
