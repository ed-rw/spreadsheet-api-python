import enum
from pydantic import BaseModel


class NewSpreadsheet(BaseModel):
    name: str


class UpdateSpreadsheet(BaseModel):
    name: str


class CellType(enum.Enum):
    LITERAL = "literal"  # literal is the only support cell type at this time


class UpdateCell(BaseModel):
    value: str
    type: CellType
