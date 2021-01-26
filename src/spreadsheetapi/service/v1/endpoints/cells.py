from fastapi import Depends
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
        cells = await handler.retrieve_data(get_cells_query)

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
        cell = await handler.retrieve_data(get_cell_query)

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
        await handler.execute(update_cell_cmd)

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
        await handler.execute(delete_cell_cmd)

        return ""
