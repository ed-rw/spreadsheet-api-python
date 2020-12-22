from pydantic import BaseModel

class NewSpreadsheet(BaseModel):
    name: str
