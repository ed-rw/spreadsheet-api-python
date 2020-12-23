class CellsEndpoint:

    uri = "/v1/spreadsheets/{spreadsheet_id}/cells"

    @staticmethod
    async def get():
        return "", 501


class CellEndpoint:

    uri = "/v1/spreadsheets/{spreadsheet_id}/cells/{cell_id}"

    @staticmethod
    async def get():
        return "", 501

    @staticmethod
    async def put():
        return "", 501
