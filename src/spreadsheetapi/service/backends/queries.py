from dataclasses import dataclass
import config


@dataclass
class RetrieveCell:
    settings: config.Settings
    spreadsheet_id: str
    cell_name: str


@dataclass
class RetrieveCells:
    settings: config.Settings
    spreadsheet_id: str


@dataclass
class RetrieveSpreadsheet:
    settings: config.Settings
    id: str


@dataclass
class RetrieveSpreadsheets:
    settings: config.Settings


@dataclass
class RetrieveSpreadsheetView:
    settings: config.Settings
    id: str
