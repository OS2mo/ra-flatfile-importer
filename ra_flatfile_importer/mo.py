#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from typing import cast
from typing import Optional
from uuid import UUID

import click
from mo_flatfile_gen import generate_mo_flatfile
from mo_flatfile_model import concat_chunk
from mo_flatfile_model import MOFlatFileFormatImport
from pydantic import AnyHttpUrl
from raclients.mo import ModelClient
from util import async_to_sync
from util import model_validate_helper
from util import takes_json_file
from util import validate_url


def mo_validate_helper(json_file) -> MOFlatFileFormatImport:
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
def validate(json_file) -> None:
    """Validate the provided JSON file."""
    mo_validate_helper(json_file)


@mo.command()
@click.option(
    "--indent", help="Pass 'indent' to json serializer", type=click.INT, default=None
)
def schema(indent: int) -> None:
    """Generate JSON schema for validate files."""
    click.echo(MOFlatFileFormatImport.schema_json(indent=indent))


@mo.command()
@click.option(
    "--mo-url",
    default="http://localhost:5000",
    show_default=True,
    callback=validate_url,
    help="Address of the OS2mo host",
)
@click.option(
    "--saml-token",
    type=click.UUID,
    help="Address of the OS2mo host",
)
@takes_json_file
@async_to_sync
async def upload(json_file, mo_url: AnyHttpUrl, saml_token: Optional[UUID]) -> None:
    """Validate the provided JSON file and upload its contents."""
    flatfilemodel = mo_validate_helper(json_file)

    client = ModelClient(base_url=mo_url, saml_token=saml_token)
    async with client.context():
        for chunk in flatfilemodel:
            objs = list(concat_chunk(chunk))
            if objs:
                print(await client.load_mo_objs(objs))


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
    flatfile = generate_mo_flatfile(name)
    click.echo(flatfile.json(indent=indent))
