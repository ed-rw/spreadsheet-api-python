import uuid

from fastapi import Depends, Response, status
from fastapi.responses import JSONResponse

from backends import exc
from backends.abstracts import QueryFactory, CommandFactory
import config
from v1 import models
from v1.endpoints import utils


class SpreadsheetsEndpoint:

    uri = "/v1/spreadsheets"

    @staticmethod
    async def get(
        settings: config.Settings = Depends(config.get_settings),
        query_factory: QueryFactory = Depends(utils.get_query_factory),
    ):
        """Return available spreadsheets"""

        get_spreadsheets_query, handler = query_factory.build(
            "RetrieveSpreadsheets", settings
        )
        spreadsheets = await handler.retrieve_data(get_spreadsheets_query)

        return spreadsheets

    @staticmethod
    async def post(
        new_spreadsheet: models.NewSpreadsheet,
        response: Response,
        settings: config.Settings = Depends(config.get_settings),
        command_factory: CommandFactory = Depends(utils.get_command_factory),
    ):
        """Create a new spreadsheet"""

        id = str(uuid.uuid4())
        create_spreadsheet_cmd, handler = command_factory.build(
            "CreateSpreadsheet", settings, id, new_spreadsheet.name
        )
        await handler.execute(create_spreadsheet_cmd)

        response.status_code = status.HTTP_201_CREATED
        return {"id": id}


class SpreadsheetEndpoint:

    uri = "/v1/spreadsheets/{spreadsheet_id}"

    @staticmethod
    async def get(
        spreadsheet_id: str,
        settings: config.Settings = Depends(config.get_settings),
        query_factory: QueryFactory = Depends(utils.get_query_factory),
    ):
        """Return the information for the given spreadsheet"""

        get_spreadsheet_query, handler = query_factory.build(
            "RetrieveSpreadsheet", settings, spreadsheet_id
        )

        try:
            spreadsheet = await handler.retrieve_data(get_spreadsheet_query)
        except exc.UnknownSpreadsheetId as e:
            return JSONResponse(status_code=404, content={"error": str(e)})

        return spreadsheet

    @staticmethod
    async def delete(
        spreadsheet_id: str,
        settings: config.Settings = Depends(config.get_settings),
        command_factory: CommandFactory = Depends(utils.get_command_factory),
    ):
        delete_spreadsheet_cmd, handler = command_factory.build(
            "DeleteSpreadsheet", settings, spreadsheet_id
        )
        await handler.execute(delete_spreadsheet_cmd)

        return ""

    @staticmethod
    async def put(
        spreadsheet_id: str,
        new_spreadsheet_data: models.UpdateSpreadsheet,
        settings: config.Settings = Depends(config.get_settings),
        command_factory: CommandFactory = Depends(utils.get_command_factory),
    ):
        update_spreadsheet_cmd, handler = command_factory.build(
            "UpdateSpreadsheet",
            settings,
            spreadsheet_id,
            dict(new_spreadsheet_data),
        )

        try:
            await handler.execute(update_spreadsheet_cmd)
        except exc.UnknownSpreadsheetId as e:
            return JSONResponse(status_code=404, content={"error": str(e)})

        return {"id": spreadsheet_id}
