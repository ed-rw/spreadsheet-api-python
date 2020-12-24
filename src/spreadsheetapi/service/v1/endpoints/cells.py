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

        get_cells_query = query_factory.build(
            "RetrieveCells", settings, spreadsheet_id
        )
        cells = get_cells_query.retrieve_data()

        return cells


class CellEndpoint:

    uri = "/v1/spreadsheets/{spreadsheet_id}/cells/{cell_id}"

    @staticmethod
    async def get(
        spreadsheet_id: str,
        cell_id: str,
        settings: config.Settings = Depends(config.get_settings),
        query_factory: QueryFactory = Depends(utils.get_query_factory),
    ):
        """Return the information for the given spreadsheet"""

        get_cell_query = query_factory.build(
            "RetrieveCell", settings, spreadsheet_id, cell_id
        )
        cell = get_cell_query.retrieve_data()

        return cell

    @staticmethod
    async def put(
        spreadsheet_id: str,
        cell_id: str,
        cell_data: models.UpdateCell,
        settings: config.Settings = Depends(config.get_settings),
        command_factory: CommandFactory = Depends(utils.get_command_factory),
    ):
        update_cell_cmd = command_factory.build(
            "UpdateCell", settings, spreadsheet_id, cell_id, cell_data
        )
        update_cell_cmd.execute()

        return ""

    @staticmethod
    async def delete(
        spreadsheet_id: str,
        cell_id: str,
        settings: config.Settings = Depends(config.get_settings),
        command_factory: CommandFactory = Depends(utils.get_command_factory),
    ):
        delete_cell_cmd = command_factory.build(
            "DeleteCell", settings, spreadsheet_id, cell_id
        )
        delete_cell_cmd.execute()

        return ""
