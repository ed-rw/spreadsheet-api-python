class UnknownSpreadsheetId(Exception):
    def __init__(self, id):
        self.unknown_id = id

    def __str__(self):
        return (
            f"{self.__class__.__name__}: Unable to find spreadsheet with "
            f"id {self.unknown_id}"
        )


class UnsupportedOperationForBackend(NotImplementedError):
    pass
