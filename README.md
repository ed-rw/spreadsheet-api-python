# spreadsheet-api-python

## Development Considerations
### Endpoints
Missing Flask's [class based views](https://flask.palletsprojects.com/en/1.1.x/views/#method-based-dispatching) here. Current using classes just as containers for static methods that are functions for each HTTP method the uri implements. Registration is done automatically in the endpoints package \_\_init__.py using a little bit of introspection/reflection..

TODO
- Have a base class for Endpoints that is aware of subclasses and registers them with the app when initialized? could be an interesting solution
