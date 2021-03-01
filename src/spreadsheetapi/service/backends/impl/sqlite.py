import json
import uuid
import databases
import sqlalchemy
from sqlalchemy.orm import Query
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Union, Optional
from backends import abstracts, commands, exc, queries, transforms

metadata = sqlalchemy.MetaData()


# DB Tables
Base = declarative_base()


class Spreadsheets(Base):
    __tablename__ = "spreadsheets"
    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)


spreadsheets = Spreadsheets.__table__


class Cells(Base):
    __tablename__ = "cells"

    # NOTE: This column is somewhat redundant, rows are uniquely
    # identified by spreadsheet_id and cell_name. SQLAlchemy doesnt allow you
    # to have a composite key as a primary key though.
    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    spreadsheet_id = sqlalchemy.Column(
        sqlalchemy.String, sqlalchemy.ForeignKey("spreadsheets.id")
    )
    name = sqlalchemy.Column(sqlalchemy.String)
    data = sqlalchemy.Column(sqlalchemy.String)

    __tableargs__ = (
        sqlalchemy.UniqueConstraint(
            "spreadsheet_id", "cell_name", name="uc_spreadsheet_cell"
        ),
    )


cells = Cells.__table__

# DB Connection Manager
class DBConnection:
    _state = {
        "db_url": None,
        "connection": None,
        "engine": None,
        "setup_done": False,
        "connected": False,
    }

    def __init__(self, db_url: str):

        self.__dict__ = DBConnection._state

        if self.db_url is not None and self.db_url != db_url:
            raise RuntimeError("Mismatched db urls")

        if not self.setup_done:
            self.setup(db_url)

    def setup(self, db_url: str):
        self.db_url = db_url
        self.engine = sqlalchemy.create_engine(
            db_url, connect_args={"check_same_thread": False}
        )
        # Create the DB schema, if necessary
        Base.metadata.create_all(self.engine)
        # Setup databases
        self.database = databases.Database(db_url)

    async def execute(
        self,
        query: Union[str, Query],
        values: Optional[Union[dict, List[dict]]] = None,
    ) -> None:
        """Execute a SQL query, this does not return any results from the
        database, generally used for DML
        """
        if not self.connected:
            await self.database.connect()
            self.connected = True

        await self.database.execute(query=query, values=values)

    async def fetch(self, query: Union[str, Query]):
        """Execute a SQL query that selects data from the database."""
        if not self.connected:
            await self.database.connect()
            self.connected = True

        return await self.database.fetch_all(query=query)


class SqliteCommandHandler(abstracts.CommandHandler):
    def __init__(self, db: DBConnection):
        self.db = db


class SqliteQueryHandler(abstracts.QueryHandler):
    def __init__(self, db: DBConnection):
        self.db = db


class NonExistantSpreadsheetMixin:
    async def _raise_for_non_existant_spreadsheet(self, settings, id):
        # This will raise an exception if the spreadsheet doesn't exist,
        # otherwise we have no need for the response.
        await RetrieveSpreadsheetHandler(self.db).retrieve_data(
            queries.RetrieveSpreadsheet(settings=settings, id=id)
        )


# Queries and Commands
class RetrieveSpreadsheetsHandler(SqliteQueryHandler):
    async def retrieve_data(self, query: queries.RetrieveSpreadsheets):
        results = await self.db.fetch(spreadsheets.select())

        return results


class RetrieveSpreadsheetHandler(SqliteQueryHandler):
    async def retrieve_data(self, query: queries.RetrieveSpreadsheet):
        results = await self.db.fetch(
            sqlalchemy.sql.select(
                [spreadsheets.c.id, spreadsheets.c.name]
            ).where(spreadsheets.c.id == query.id)
        )
        if len(results) == 0:
            raise exc.UnknownSpreadsheetId(query.id)
        else:
            return results[0]


class RetrieveSpreadsheetViewHandler(SqliteQueryHandler):
    async def retrieve_data(self, query: queries.RetrieveSpreadsheetView):
        cells = await RetrieveCellsHandler(self.db).retrieve_data(
            queries.RetrieveCells(
                settings=query.settings, spreadsheet_id=query.id
            )
        )

        cells_transform = transforms.CellsToView(cells)
        return cells_transform.view()


class CreateSpreadsheetHandler(SqliteCommandHandler):
    async def execute(self, cmd: commands.CreateSpreadsheet):
        sql = spreadsheets.insert()
        values = {"name": cmd.name, "id": cmd.id}
        await self.db.execute(sql, values)


class DeleteSpreadsheetHandler(SqliteCommandHandler):
    async def execute(self, cmd: commands.DeleteSpreadsheet):
        sql = cells.delete().where(cells.c.spreadsheet_id == cmd.id)
        await self.db.execute(sql)

        sql = spreadsheets.delete().where(spreadsheets.c.id == cmd.id)
        await self.db.execute(sql)


class UpdateSpreadsheetHandler(
    SqliteCommandHandler, NonExistantSpreadsheetMixin
):
    async def execute(self, cmd: commands.UpdateSpreadsheet):
        await self._raise_for_non_existant_spreadsheet(cmd.settings, cmd.id)

        sql = (
            spreadsheets.update()
            .where(spreadsheets.c.id == cmd.id)
            .values(**cmd.new_spreadsheet_data)
        )
        await self.db.execute(sql, cmd.new_spreadsheet_data)


class RetrieveCellsHandler(SqliteQueryHandler, NonExistantSpreadsheetMixin):
    async def retrieve_data(self, query: queries.RetrieveCells) -> List[dict]:

        await self._raise_for_non_existant_spreadsheet(
            query.settings, query.spreadsheet_id
        )

        results = await self.db.fetch(
            sqlalchemy.sql.select([cells.c.name, cells.c.data]).where(
                cells.c.spreadsheet_id == query.spreadsheet_id
            )
        )

        # Deserialize json in cell "data" column
        def transform_row(row) -> dict:
            row = {**row}
            row["data"] = json.loads(row["data"])
            return row

        return [transform_row(row) for row in results]


class RetrieveCellHandler(SqliteQueryHandler, NonExistantSpreadsheetMixin):
    async def retrieve_data(
        self, query: queries.RetrieveCell
    ) -> Optional[dict]:

        await self._raise_for_non_existant_spreadsheet(
            query.settings, query.spreadsheet_id
        )

        sql = (
            sqlalchemy.sql.select([cells.c.name, cells.c.data])
            .where(cells.c.spreadsheet_id == query.spreadsheet_id)
            .where(cells.c.name == query.cell_name,)
        )
        results = await self.db.fetch(sql)
        if len(results) == 0:
            return None
        else:
            row = {**results[0]}
            row["data"] = json.loads(row["data"])
            return row


class UpdateCellHandler(SqliteCommandHandler, NonExistantSpreadsheetMixin):
    async def execute(self, cmd: commands.UpdateCell):

        await self._raise_for_non_existant_spreadsheet(
            cmd.settings, cmd.spreadsheet_id
        )

        # TODO: switch to upsert
        sql = (
            sqlalchemy.sql.select([cells.c.id])
            .where(cells.c.spreadsheet_id == cmd.spreadsheet_id)
            .where(cells.c.name == cmd.cell_name,)
        )
        results = await self.db.fetch(sql)
        if len(results) == 0:
            await self._insert(cmd)
        else:
            await self._update(cmd)

    async def _insert(self, cmd: commands.UpdateCell):
        sql = cells.insert()
        value = {
            "spreadsheet_id": cmd.spreadsheet_id,
            "name": cmd.cell_name,
            "id": str(uuid.uuid4()),
            "data": cmd.new_cell_data.json(),
        }
        await self.db.execute(sql, value)

    async def _update(self, cmd: commands.UpdateCell):
        sql = (
            cells.update()
            .where(cells.c.spreadsheet_id == cmd.spreadsheet_id)
            .where(cells.c.name == cmd.cell_name,)
            .values(data=cmd.new_cell_data.json())
        )
        await self.db.execute(sql, {"data": cmd.new_cell_data.json()})


class DeleteCellHandler(SqliteCommandHandler, NonExistantSpreadsheetMixin):
    async def execute(self, cmd: commands.DeleteCell):
        await self._raise_for_non_existant_spreadsheet(
            cmd.settings, cmd.spreadsheet_id
        )

        sql = (
            cells.delete()
            .where(cells.c.spreadsheet_id == cmd.spreadsheet_id)
            .where(cells.c.name == cmd.cell_name,)
        )
        await self.db.execute(sql)


# Factories
class SQLiteQueryFactory(abstracts.QueryFactory):
    handler_map = {
        "RetrieveSpreadsheets": RetrieveSpreadsheetsHandler,
        "RetrieveSpreadsheet": RetrieveSpreadsheetHandler,
        "RetrieveSpreadsheetView": RetrieveSpreadsheetViewHandler,
        "RetrieveCell": RetrieveCellHandler,
        "RetrieveCells": RetrieveCellsHandler,
    }

    def __init__(self, settings):
        super().__init__(settings)
        self.db = DBConnection(settings.backend_db_url)

    def get_handler(self, query_name: str):
        return self.handler_map[query_name](self.db)


class SQLiteCommandFactory(abstracts.CommandFactory):
    handler_map = {
        "CreateSpreadsheet": CreateSpreadsheetHandler,
        "DeleteSpreadsheet": DeleteSpreadsheetHandler,
        "UpdateSpreadsheet": UpdateSpreadsheetHandler,
        "UpdateCell": UpdateCellHandler,
        "DeleteCell": DeleteCellHandler,
    }

    def __init__(self, settings):
        super().__init__(settings)
        self.db = DBConnection(settings.backend_db_url)

    def get_handler(self, command_name: str):
        return self.handler_map[command_name](self.db)
