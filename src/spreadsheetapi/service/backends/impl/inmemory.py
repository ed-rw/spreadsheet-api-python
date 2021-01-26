import config
from backends import abstracts, commands, queries

spreadsheets = {}  # Map spreadsheet id to dict of metadata
cells = {}  # Map spreadsheet id to dict, this maps cell ids to
# cell data.


class RetrieveSpreadsheetsHandler(abstracts.QueryHandler):
    async def retrieve_data(self, query: queries.RetrieveSpreadsheets):
        return spreadsheets


class RetrieveSpreadsheetHandler(abstracts.QueryHandler):
    async def retrieve_data(self, query: queries.RetrieveSpreadsheet):
        return spreadsheets[query.spreadsheet_id]


class CreateSpreadsheetHandler(abstracts.CommandHandler):
    async def execute(self, cmd: commands.CreateSpreadsheet):
        spreadsheets[cmd.id] = {"name": cmd.name}
        cells[cmd.id] = {}


class DeleteSpreadsheetHandler(abstracts.CommandHandler):
    async def execute(self, cmd: commands.DeleteSpreadsheet):
        del spreadsheets[cmd.id]
        del cells[cmd.id]


class UpdateSpreadsheetHandler(abstracts.CommandHandler):
    async def execute(self, cmd: commands.UpdateSpreadsheet):
        spreadsheets[cmd.id] = cmd.new_spreadsheet_data


class RetrieveCellsHandler(abstracts.QueryHandler):
    async def retrieve_data(self, query: queries.RetrieveCells):
        return cells[query.spreadsheet_id]


class RetrieveCellHandler(abstracts.QueryHandler):
    async def retrieve_data(self, query: queries.RetrieveCell):
        return cells[query.spreadsheet_id].get(query.cell_name)


class UpdateCellHandler(abstracts.CommandHandler):
    async def execute(self, cmd: commands.UpdateCell):
        cells[cmd.spreadsheet_id][cmd.cell_name] = cmd.new_cell_data


class DeleteCellHandler(abstracts.CommandHandler):
    async def execute(self, cmd: commands.DeleteCell):
        del cells[cmd.spreadsheet_id][cmd.cell_name]


class InMemoryQueryFactory(abstracts.QueryFactory):
    handler_map = {
        "RetrieveSpreadsheets": RetrieveSpreadsheetsHandler,
        "RetrieveSpreadsheet": RetrieveSpreadsheetHandler,
        "RetrieveCell": RetrieveCellHandler,
        "RetrieveCells": RetrieveCellsHandler,
    }

    def get_handler(self, query_name: str):
        return self.handler_map[query_name]()


class InMemoryCommandFactory(abstracts.CommandFactory):
    handler_map = {
        "CreateSpreadsheet": CreateSpreadsheetHandler,
        "DeleteSpreadsheet": DeleteSpreadsheetHandler,
        "UpdateSpreadsheet": UpdateSpreadsheetHandler,
        "UpdateCell": UpdateCellHandler,
        "DeleteCell": DeleteCellHandler,
    }

    def get_handler(self, command_name: str):
        return self.handler_map[command_name]()
