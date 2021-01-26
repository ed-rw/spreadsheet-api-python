from .impl.inmemory import InMemoryCommandFactory, InMemoryQueryFactory
from .impl.sqlite import SQLiteCommandFactory, SQLiteQueryFactory

backend_command_factories = {
    "InMemory": InMemoryCommandFactory,
    "SQLite": SQLiteCommandFactory,
}

backend_query_factories = {
    "InMemory": InMemoryQueryFactory,
    "SQLite": SQLiteQueryFactory,
}
