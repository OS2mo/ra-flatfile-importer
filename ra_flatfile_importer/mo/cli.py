#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import asyncio
from typing import cast
from typing import TextIO

import click
from pydantic import AnyHttpUrl

from ra_flatfile_importer.mo.generator import generate_mo_flatfile
from ra_flatfile_importer.mo.models import MOFlatFileFormatImport
from ra_flatfile_importer.mo.uploader import upload as mo_upload
from ra_flatfile_importer.util import model_validate_helper
from ra_flatfile_importer.util import takes_json_file
from ra_flatfile_importer.util import validate_url


def mo_validate_helper(json_file: TextIO) -> MOFlatFileFormatImport:
    return cast(
        MOFlatFileFormatImport, model_validate_helper(MOFlatFileFormatImport, json_file)
    )


@click.group()
def mo() -> None:
    """OS2mo Flatfile importer.

    Used to validate and load flatfile data (JSON) into OS2mo.
    """
    pass


@mo.command()
@takes_json_file
def validate(json_file: TextIO) -> None:
    """Validate the provided JSON file."""
    mo_validate_helper(json_file)


@mo.command()
@click.option(
    "--indent", help="Pass 'indent' to json serializer", type=click.INT, default=None
)
def schema(indent: int) -> None:
    """Generate JSON schema for valid files."""
    click.echo(MOFlatFileFormatImport.schema_json(indent=indent))


@mo.command()
@click.option(
    "--mo-url",
    default="http://localhost:5000",
    show_default=True,
    callback=validate_url,
    help="Address of the OS2mo host",
)
@takes_json_file
def upload(json_file: TextIO, mo_url: AnyHttpUrl) -> None:
    """Validate the provided JSON file and upload its contents."""
    flat_file_import = mo_validate_helper(json_file)
    asyncio.run(mo_upload(flat_file_import, mo_url))


@mo.command()
@click.option(
    "--name",
    help="Name of the root organization",
    required=True,
)
@click.option(
    "--indent", help="Pass 'indent' to json serializer", type=click.INT, default=None
)
def generate(name: str, indent: int) -> None:
    """Generate OS2mo fixture."""
    flatfile = generate_mo_flatfile(name)
    click.echo(flatfile.json(indent=indent))
