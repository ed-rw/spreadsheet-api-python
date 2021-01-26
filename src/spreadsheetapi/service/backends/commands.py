from dataclasses import dataclass
import config


@dataclass
class CreateSpreadsheet:
    settings: config.Settings
    id: str
    name: str


@dataclass
class DeleteSpreadsheet:
    settings: config.Settings
    id: str


@dataclass
class DeleteCell:
    settings: config.Settings
    spreadsheet_id: str
    cell_name: str


@dataclass
class UpdateCell:
    settings: config.Settings
    spreadsheet_id: str
    cell_name: str
    new_cell_data: dict


@dataclass
class UpdateSpreadsheet:
    settings: config.Settings
    id: str
    new_spreadsheet_data: dict
