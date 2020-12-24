import config
from backends import abstracts

spreadsheets = {}  # Map spreadsheet id to dict of metadata
cells = {}  # Map spreadsheet id to dict, this maps cell ids to
# cell data.


class RetrieveSpreadsheets(abstracts.RetrieveSpreadsheets):
    def retrieve_data(self):
        return spreadsheets


class RetrieveSpreadsheet(abstracts.RetrieveSpreadsheet):
    def retrieve_data(self):
        return spreadsheets[self.spreadsheet_id]


class CreateSpreadsheet(abstracts.CreateSpreadsheet):
    def execute(self):
        spreadsheets[self.id] = {"name": self.name}
        cells[self.id] = {}


class DeleteSpreadsheet(abstracts.DeleteSpreadsheet):
    def execute(self):
        del spreadsheets[self.id]
        del cells[self.id]


class UpdateSpreadsheet(abstracts.UpdateSpreadsheet):
    def execute(self):
        spreadsheets[self.id] = self.new_spreadsheet_data


class RetrieveCells(abstracts.RetrieveCells):
    def retrieve_data(self):
        return cells[self.spreadsheet_id]


class RetrieveCell(abstracts.RetrieveCell):
    def retrieve_data(self):
        return cells[self.spreadsheet_id][self.cell_id]


class UpdateCell(abstracts.UpdateCell):
    def execute(self):
        cells[self.spreadsheet_id][self.cell_id] = self.new_cell_data


class InMemoryQueryFactory(abstracts.QueryFactory):
    def __init__(self, settings):
        super().__init__(settings)
        self.query_map = {
            "RetrieveSpreadsheets": RetrieveSpreadsheets,
            "RetrieveSpreadsheet": RetrieveSpreadsheet,
            "RetrieveCell": RetrieveCell,
            "RetrieveCells": RetrieveCells,
        }


class InMemoryCommandFactory(abstracts.CommandFactory):
    def __init__(self, settings):
        super().__init__(settings)
        self.command_map = {
            "CreateSpreadsheet": CreateSpreadsheet,
            "DeleteSpreadsheet": DeleteSpreadsheet,
            "UpdateSpreadsheet": UpdateSpreadsheet,
            "UpdateCell": UpdateCell,
        }
