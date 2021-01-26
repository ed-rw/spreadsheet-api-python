from fastapi import Depends

from backends import backend_command_factories, backend_query_factories
import config


def get_command_factory(
    settings: config.Settings = Depends(config.get_settings),
):
    return backend_command_factories[settings.backend.value](settings)


def get_query_factory(settings: config.Settings = Depends(config.get_settings)):
    # TODO Handle improperly configured backend,
    # TODO use introspection instead of maps
    return backend_query_factories[settings.backend.value](settings)
