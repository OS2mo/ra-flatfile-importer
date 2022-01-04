# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
FROM python:3.9

WORKDIR /app

ENV POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python --

COPY pyproject.toml poetry.lock* ./

RUN /opt/poetry/bin/poetry install --no-root --no-dev

COPY . ./

ENTRYPOINT ["python", "-m", "ra_flatfile_importer"]
