from fastapi import Depends
from fastapi.responses import JSONResponse, PlainTextResponse

from backends import exc
from backends.abstracts import QueryFactory
import config
from v1 import models
from v1.endpoints import utils


class SpreadsheetViewEndpoint:

    uri = "/v1/spreadsheets/{spreadsheet_id}/view"

    @staticmethod
    async def get(
        spreadsheet_id: str,
        settings: config.Settings = Depends(config.get_settings),
        query_factory: QueryFactory = Depends(utils.get_query_factory),
    ):
        """Return a tab separated view of the cells in the spreadsheet"""

        spreadsheet_view_query, handler = query_factory.build(
            "RetrieveSpreadsheetView", settings, spreadsheet_id
        )
        try:
            view = await handler.retrieve_data(spreadsheet_view_query)
        except exc.UnknownSpreadsheetId as e:
            return JSONResponse(status_code=404, content={"error": str(e)})

        # Not serializing this as json as it is meant to just pop out as plain
        # text in a browser or on the command line.
        return PlainTextResponse(view)
