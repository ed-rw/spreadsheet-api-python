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


class DeleteSpreadsheet(Command, ABC):
    def __init__(self, settings: config.Settings, id: str):
        self.settings = settings
        self.id = id

    @abstractmethod
    def execute(self):
        pass


class UpdateCell(Command, ABC):
    def __init__(
        self,
        settings: config.Settings,
        spreadsheet_id: str,
        cell_id: str,
        new_cell_data: dict,
    ):
        self.spreadsheet_id = spreadsheet_id
        self.cell_id = cell_id
        self.new_cell_data = new_cell_data

    @abstractmethod
    def execute(self):
        pass


class UpdateSpreadsheet(Command, ABC):
    def __init__(
        self, settings: config.Settings, id: str, new_spreadsheet_data: dict
    ):
        self.settings = settings
        self.id = id
        self.new_spreadsheet_data = new_spreadsheet_data

    @abstractmethod
    def execute(self):
        pass


class RetrieveCell(Query, ABC):
    def __init__(
        self, settings: config.Settings, spreadsheet_id: str, cell_id: str
    ):
        self.spreadsheet_id = spreadsheet_id
        self.cell_id = cell_id

    @abstractmethod
    def retrieve_data(self):
        pass


class RetrieveCells(Query, ABC):
    def __init__(self, settings: config.Settings, spreadsheet_id: str):
        self.spreadsheet_id = spreadsheet_id

    @abstractmethod
    def retrieve_data(self):
        pass


class RetrieveSpreadsheet(Query, ABC):
    def __init__(self, settings: config.Settings, spreadsheet_id: str):
        elf.spreadsheet_id = spreadsheet_id

    @abstractmethod
    def retrieve_data(self):
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
