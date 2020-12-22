from .inmemory import InMemoryCommandFactory, InMemoryQueryFactory

backend_command_factories = {
    "InMemory": InMemoryCommandFactory
}

backend_query_factories = {
    "InMemory": InMemoryQueryFactory
}
