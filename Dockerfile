FROM python:3.8-slim as build

RUN set -xe && \
    apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get purge -y --auto-remove && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN set -xe && \
    pip install -U pip && \
    pip install -U pipenv pbr

COPY Pipfile* ./

RUN pipenv lock -r > requirements.txt

COPY . .

RUN pipenv run python setup.py bdist_wheel

FROM python:3.8-slim as app

WORKDIR /app

ENV ROOT_PATH_FOR_DYNACONF=/app

RUN set -xe && \
    apt-get update -q && \
    apt-get upgrade -y -q && \
    apt-get purge -y --auto-remove && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

COPY --from=build /app/dist/*.whl .

RUN set -xe && \
    pip install *.whl && \
    rm -f *.whl

COPY settings.toml .

ENTRYPOINT ["dypendence", "main"]
