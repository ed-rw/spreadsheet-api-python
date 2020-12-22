
import config
from backends import abstracts

spreadsheets = {}  # Map spreadsheet id to dict of metadata
cells = {}  # Map spreadsheet id to dict, this maps cell ids to
            # cell data.


class CreateSpreadsheet(abstracts.CreateSpreadsheet):
    def execute(self):
        spreadsheets[self.id] = {"name": self.name}


class RetrieveSpreadsheets(abstracts.RetrieveSpreadsheets):
    def retrieve_data(self):
        return spreadsheets


class InMemoryQueryFactory(abstracts.QueryFactory):
    def __init__(self, settings):
        super().__init__(settings)
        self.query_map = {'RetrieveSpreadsheets': RetrieveSpreadsheets}


class InMemoryCommandFactory(abstracts.CommandFactory):
    def __init__(self, settings):
        super().__init__(settings)
        self.command_map = {'CreateSpreadsheet': CreateSpreadsheet}
