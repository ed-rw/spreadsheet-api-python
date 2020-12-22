import uuid

from fastapi import Depends, Response, status

from backends.abstracts import QueryFactory, CommandFactory
import config
from v1 import models
from v1.endpoints import utils

class SpreadsheetsEndpoint:

    uri = '/v1/spreadsheets'

    @staticmethod
    async def get(settings: config.Settings = Depends(config.get_settings),
                  query_factory: QueryFactory = Depends(utils.get_query_factory)):
        """Return available spreadsheets"""

        get_spreadsheets_query =  query_factory.build('RetrieveSpreadsheets',
                                                      settings)
        spreadsheets = get_spreadsheets_query.retrieve_data()

        return spreadsheets

    @staticmethod
    async def post(new_spreadsheet: models.NewSpreadsheet, response: Response,
                   settings: config.Settings = Depends(config.get_settings),
                   command_factory: CommandFactory = Depends(utils.get_command_factory)):
        """Create a new spreadsheet"""

        id = uuid.uuid4()
        create_spreadsheet_cmd = command_factory.build('CreateSpreadsheet',
                settings, id, new_spreadsheet.name
            )
        create_spreadsheet_cmd.execute()

        response.status_code = status.HTTP_201_CREATED
        return {"id": id}

class SpreadsheetEndpoint:

    uri = '/v1/spreadsheets/{spreadsheet_id}'

    @staticmethod
    async def get(spreadsheet_id: str):
        """Return the information for the given spreadsheet"""
        return {"id": "dfs", "name": "Spreadsheet 1"}, 501

    @staticmethod
    async def delete(spreadsheet_id: str):
        return "", 501

    @staticmethod
    async def put(spreadsheet_id: str):
        return "", 501
