from fastapi import Depends
from fastapi.responses import JSONResponse

from backends import exc
from backends.abstracts import QueryFactory, CommandFactory
import config
from v1 import models
from v1.endpoints import utils


class CellsEndpoint:

    uri = "/v1/spreadsheets/{spreadsheet_id}/cells"

    @staticmethod
    async def get(
        spreadsheet_id: str,
        settings: config.Settings = Depends(config.get_settings),
        query_factory: QueryFactory = Depends(utils.get_query_factory),
    ):
        """Return the information for the given spreadsheet"""

        get_cells_query, handler = query_factory.build(
            "RetrieveCells", settings, spreadsheet_id
        )

        try:
            cells = await handler.retrieve_data(get_cells_query)
        except exc.UnknownSpreadsheetId as e:
            return JSONResponse(status_code=404, content={"error": str(e)})

        return cells


class CellEndpoint:

    uri = "/v1/spreadsheets/{spreadsheet_id}/cells/{cell_name}"

    @staticmethod
    async def get(
        spreadsheet_id: str,
        cell_name: str,
        settings: config.Settings = Depends(config.get_settings),
        query_factory: QueryFactory = Depends(utils.get_query_factory),
    ):
        """Return the information for the given spreadsheet"""

        get_cell_query, handler = query_factory.build(
            "RetrieveCell", settings, spreadsheet_id, cell_name
        )

        try:
            cell = await handler.retrieve_data(get_cell_query)
        except exc.UnknownSpreadsheetId as e:
            return JSONResponse(status_code=404, content={"error": str(e)})

        return cell

    @staticmethod
    async def put(
        spreadsheet_id: str,
        cell_name: str,
        cell_data: models.UpdateCell,
        settings: config.Settings = Depends(config.get_settings),
        command_factory: CommandFactory = Depends(utils.get_command_factory),
    ):

        update_cell_cmd, handler = command_factory.build(
            "UpdateCell", settings, spreadsheet_id, cell_name, cell_data
        )

        try:
            await handler.execute(update_cell_cmd)
        except exc.UnknownSpreadsheetId as e:
            return JSONResponse(status_code=404, content={"error": str(e)})

        return ""

    @staticmethod
    async def delete(
        spreadsheet_id: str,
        cell_name: str,
        settings: config.Settings = Depends(config.get_settings),
        command_factory: CommandFactory = Depends(utils.get_command_factory),
    ):
        delete_cell_cmd, handler = command_factory.build(
            "DeleteCell", settings, spreadsheet_id, cell_name
        )

        try:
            await handler.execute(delete_cell_cmd)
        except exc.UnknownSpreadsheetId as e:
            return JSONResponse(status_code=404, content={"error": str(e)})

        return ""
