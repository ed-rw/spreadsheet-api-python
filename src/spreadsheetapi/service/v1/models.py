from pydantic import BaseModel


class NewSpreadsheet(BaseModel):
    name: str


class UpdateSpreadsheet(BaseModel):
    name: str


class UpdateCell(BaseModel):
    value: str
    type: str
