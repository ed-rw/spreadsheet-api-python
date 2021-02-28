FROM python:3.8-alpine

# This Dockerfile is intended to be built from the root of the repository
COPY service/ /opt/spreadsheetapi/service
COPY Pipfile /opt/spreadsheetapi/Pipfile
COPY Pipfile.lock /opt/spreadsheetapi/Pipfile.lock

RUN pip install pipenv && \
    cd /opt/spreadsheetapi && \
    pipenv install --system --deploy --ignore-pipfile

EXPOSE 8080
WORKDIR /opt/spreadsheetapi/service

CMD ["uvicorn", "application:app", "--host", "0.0.0.0", "--port", "8080"]
