# spreadsheet-api-python

This is intended to serve as an API backend with pluggable storage for a
web-based spreadsheet application. I've chosen to build a spreadsheet
application since it is easy to start simply, and later layer in complexity
(_e.g._ data formatting, calculated values, websockets, concurrent editing).

This application will be implemented as a set of individual repositories
and components in order to allow the use of various languages and frameworks.
This also mimics a microservices system architecture, and will allow
experimentation with different testing and deployment strategies.

While this is the first, I hope to include the following components:
- spreadsheet-frontend-svelte
- spreadsheet-frontend-vue
- spreadsheet-frontend-elm
- spreadsheet-api-go
- spreadsheet-api-erlang/elixir

## Related Repos
- [spreadsheet-api-tests](https://github.com/ed-rw/spreadsheet-api-tests)

## Project Setup

* Requires Python 3.8 and [pipenv](https://pipenv.pypa.io/en/latest/)

To install required Python packages navigate to the `src/spreadsheetapi`
directory and run `pipenv install`.

## Running the api server

From the `src/spreadsheetapi/service` directory run
`pipenv run uvicorn application:app`

## Interfacing with the api server

By default the server is available on port 8000 on the loopback address.

Currently the server is set to use the "InMemory" backend. All spreadsheet
data created will be cleared between runs of the server with this backend.
Switching to the Sqlite backend enables persistence. This is controlled in the
[config.py](src/spreadsheetapi/service/config.py) file.

FastAPI (the Python web framework used for this process) autogenerates swagger
documentation for the API. This is available at `http://127.0.0.1:8000/docs`.
I have not dug deeply into the information presented in this interface, so it
may be incorrect or incomplete at this time.

## CI/CD and "Production" Setup

This repository uses GitHub actions to automatically test pull requests and
commits made to the master branch. The main test suite is located in the
external repo
[spreadsheet-api-tests](https://github.com/ed-rw/spreadsheet-api-tests).

Commits to the master branch are continuously deployed to DigitalOcean's
App Platform. Commits can be excluded from deployment by starting the commit
message with `ND:` (Non-deploy commit).

This service uses Terraform to provision and configure the DigitalOcean App
Platform on which it is run. App Platform handles building and deploying the
Docker container that the service runs within. Deploys are initiated using the
DigitalOcean cli tool in the [master pipeline](.github/workflows/master.yml).

## Development Considerations
### Endpoints
Missing Flask's [class based views](https://flask.palletsprojects.com/en/1.1.x/views/#method-based-dispatching)
here. Current using classes just as containers
for static methods that are functions for each HTTP method the uri implements.
Registration is done automatically in the endpoints package \_\_init__.py using
a little bit of introspection/reflection..

## TODO
- restrict CI pipelines to only run when code changes
- remove service directory and shift contents up, will make imports clearer
- Dockerize
- config updates - from env, dependent configuration item (eg setting sqlite
   backend requires db url setting)
- Pre-commit hook for black and mypy
- Redis backend
- Have a base class for Endpoints that is aware of subclasses and registers them
with the app when initialized? could be an interesting solution
