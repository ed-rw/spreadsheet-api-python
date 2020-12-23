import importlib
import inspect
import pkgutil

from fastapi import APIRouter

router = APIRouter()

METHOD_NAMES_TO_REGISTER = ("get", "post", "put", "patch", "delete")


def register_endpoint_methods(endpoint_class):
    endpoint_class_methods = inspect.getmembers(
        endpoint_class, predicate=inspect.isfunction
    )
    for method_name, fxn_obj in endpoint_class_methods:
        if method_name in METHOD_NAMES_TO_REGISTER:
            # NOTE: The getattr call grabs the method on the router that
            # is used to register functions to a given HTTP method and
            # uri. This method is normally used as a decorator.
            getattr(router, method_name)(endpoint_class.uri)(fxn_obj)


def is_endpoint_class(member):
    return inspect.isclass(member) and member.__name__.endswith("Endpoint")


for importer, module_name, ispkg in pkgutil.iter_modules(["./v1/endpoints"]):
    if ispkg:
        print(
            f"Endpoint registration is ignoring {module} since it "
            "is a package"
        )
        continue

    module = importer.find_module(module_name).load_module(module_name)
    endpoint_classes = inspect.getmembers(module, predicate=is_endpoint_class)

    for _, class_ in endpoint_classes:
        register_endpoint_methods(class_)
