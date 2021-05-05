#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from typing import List

import click
from pydantic import AnyHttpUrl
from pydantic import BaseModel
from ramodels.lora import Facet
from ramodels.lora import Klasse
from ramodels.lora import Organisation
from util import model_validate_helper
from util import takes_json_file
from util import validate_url


class LoraFlatFileFormatModel(BaseModel):
    """Flatfile format for LoRa.

    Minimal valid example is {}.
    """

    facetter: List[Facet] = []
    klasser: List[Klasse] = []
    organisationer: List[Organisation] = []


def lora_validate_helper(json_file) -> LoraFlatFileFormatModel:
    return cast(
        LoraFlatFileFormatModel,
        model_validate_helper(LoraFlatFileFormatModel, json_file)
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
def upload(json_file, mox_url: AnyHttpUrl) -> None:
    """Validate the provided JSON file and upload its contents."""
    flatfilemodel = lora_validate_helper(json_file)
    print(flatfilemodel)
    # TODO: Upload it using Client
