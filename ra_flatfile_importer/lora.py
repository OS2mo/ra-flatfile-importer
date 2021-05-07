#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from functools import partial
from typing import cast
from typing import Type

import click
from lora_flatfile_gen import generate_lora_flatfile
from lora_flatfile_model import LoraFlatFileFormatModel
from pydantic import AnyHttpUrl
from raclients.lora import ModelClient
from ramodels.base import RABase
from util import async_to_sync
from util import model_validate_helper
from util import takes_json_file
from util import validate_url


LoraObj = Type[RABase]


def lora_validate_helper(json_file) -> LoraFlatFileFormatModel:
    return cast(
        LoraFlatFileFormatModel,
        model_validate_helper(LoraFlatFileFormatModel, json_file),
    )


@click.group()
def lora() -> None:
    """Lora Flatfile importer.

    Used to validate and load flatfile data (JSON) into LoRa.
    """
    pass


@lora.command()
@takes_json_file
def validate(json_file) -> None:
    """Validate the provided JSON file."""
    lora_validate_helper(json_file)


@lora.command()
@click.option(
    "--indent", help="Pass 'indent' to json serializer", type=click.INT, default=None
)
def schema(indent: int) -> None:
    """Generate JSON schema for validate files."""
    click.echo(LoraFlatFileFormatModel.schema_json(indent=indent))


@lora.command()
@click.option(
    "--mox-url",
    default="http://localhost:8080",
    show_default=True,
    callback=validate_url,
    help="Address of the MOX host",
)
@takes_json_file
@async_to_sync
async def upload(json_file, mox_url: AnyHttpUrl) -> None:
    """Validate the provided JSON file and upload its contents."""
    flatfilemodel = lora_validate_helper(json_file)
    order = ["organisationer", "facetter", "klasser"]
    ordered_objs = map(partial(getattr, flatfilemodel), order)
    ordered_objs = filter(None, ordered_objs)

    client = ModelClient(base_url=mox_url)
    async with client.context():
        for objs in ordered_objs:
            print(await client.load_lora_objs(objs))


@lora.command()
@click.option(
    "--name",
    help="Name of the root organization",
    required=True,
)
@click.option(
    "--indent", help="Pass 'indent' to json serializer", type=click.INT, default=None
)
def initialize(name: str, indent: int) -> None:
    """Generate LoRa initializer file."""
    flatfile = generate_lora_flatfile(name)
    click.echo(flatfile.json(indent=indent))


@lora.command()
@click.option(
    "--name",
    help="Name of the root organization",
    required=True,
)
@click.option(
    "--indent", help="Pass 'indent' to json serializer", type=click.INT, default=None
)
def generate(name: str, indent: int) -> None:
    """Generate LoRa fixture."""
    flatfile = generate_lora_flatfile(name, dummy_classes=True)
    click.echo(flatfile.json(indent=indent))
