

class SpreadsheetsEndpoint:

    uri = '/v1/spreadsheets'

    @staticmethod
    async def get():
        """Return available spreadsheets"""
        return {"spreadsheets": ['a', 'b', 'c']}

    @staticmethod
    async def post():
        """Create a new spreadsheet"""
        # create new id
        id = "some_guid"

        # create spreadsheet using new id

        return {"id": id}, 201

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
