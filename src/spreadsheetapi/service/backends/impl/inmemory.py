import config
from backends import abstracts, commands, exc, queries

spreadsheets = {}  # Map spreadsheet id to dict of metadata
cells = {}  # Map spreadsheet id to dict, this maps cell ids to
# cell data.


class RetrieveSpreadsheetsHandler(abstracts.QueryHandler):
    async def retrieve_data(self, query: queries.RetrieveSpreadsheets):
        return [{**data, "id": id} for id, data in spreadsheets.items()]


class RetrieveSpreadsheetHandler(abstracts.QueryHandler):
    async def retrieve_data(self, query: queries.RetrieveSpreadsheet):
        if query.id not in spreadsheets:
            raise exc.UnknownSpreadsheetId(query.id)

        return {**spreadsheets[query.id], "id": query.id}


class CreateSpreadsheetHandler(abstracts.CommandHandler):
    async def execute(self, cmd: commands.CreateSpreadsheet):
        spreadsheets[cmd.id] = {"name": cmd.name}
        cells[cmd.id] = {}


class DeleteSpreadsheetHandler(abstracts.CommandHandler):
    async def execute(self, cmd: commands.DeleteSpreadsheet):
        if cmd.id in spreadsheets:
            del spreadsheets[cmd.id]

        if cmd.id in cells:
            del cells[cmd.id]


class UpdateSpreadsheetHandler(abstracts.CommandHandler):
    async def execute(self, cmd: commands.UpdateSpreadsheet):
        if cmd.id not in spreadsheets:
            raise exc.UnknownSpreadsheetId(cmd.id)

        spreadsheets[cmd.id] = cmd.new_spreadsheet_data


class RetrieveCellsHandler(abstracts.QueryHandler):
    async def retrieve_data(self, query: queries.RetrieveCells):
        if query.spreadsheet_id not in spreadsheets:
            raise exc.UnknownSpreadsheetId(query.spreadsheet_id)

        return [
            {"name": name, "data": data}
            for name, data in cells[query.spreadsheet_id].items()
        ]


class RetrieveCellHandler(abstracts.QueryHandler):
    async def retrieve_data(self, query: queries.RetrieveCell):
        if query.spreadsheet_id not in spreadsheets:
            raise exc.UnknownSpreadsheetId(query.spreadsheet_id)

        data = cells[query.spreadsheet_id].get(query.cell_name)

        if data is None:
            return None
        else:
            return {"name": query.cell_name, "data": data}


class UpdateCellHandler(abstracts.CommandHandler):
    async def execute(self, cmd: commands.UpdateCell):
        if cmd.spreadsheet_id not in spreadsheets:
            raise exc.UnknownSpreadsheetId(cmd.spreadsheet_id)

        cells[cmd.spreadsheet_id][cmd.cell_name] = cmd.new_cell_data


class DeleteCellHandler(abstracts.CommandHandler):
    async def execute(self, cmd: commands.DeleteCell):
        if cmd.spreadsheet_id not in spreadsheets:
            raise exc.UnknownSpreadsheetId(cmd.spreadsheet_id)

        if cmd.cell_name in cells[cmd.spreadsheet_id]:
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
