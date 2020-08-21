

class SpreadsheetsEndpoint:

    uri = '/v1/spreadsheets'

    @staticmethod
    async def get():
        return {"spreadsheets": ['a', 'b', 'c']}
